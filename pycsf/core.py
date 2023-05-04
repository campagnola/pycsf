from collections import OrderedDict
import os, json, tempfile, weakref
import numpy as np
from pyqtgraph.Qt import QtWidgets, QtCore


IONS = OrderedDict([('Na', 1), ('K', 1), ('Cl', -1), ('Ca', 2), ('Mg', 2), ('SO4', -2), ('PO4', -3), ('Cs', 1)])


class Reagents(QtCore.QObject):
    """A table of reagents and their properties.

    Fields are:
    
        * group (str): The name of a group to which this reagent belongs.
        * name (str): The long name of this reagent.
        * formula (str): The molecular formula or short name for this reagent.
        * molweight (float): The number of grams of product per mole of reagent.
          Note that this may be different from the actual molecular weight of the
          reagent if the product contains impurities.
        * osmconst (float): Osmotic constant to use for this reagent when estimating osmolarity.
        * <ion dissociation constants> (float): For each type of ion (K, Na, Cl, ...),
          the number of free ions contributed by one molecule of this reagent. 
        * notes (str): Description of this reagent / product.
    
    Note: Each reagent is uniquely identified by its name. In a more robust
    database, we might have used a unique integer ID instead, but in this case
    we want the database json file to be human readable and editable.
    """
    sigReagentListChanged = QtCore.Signal(object)  # self
    sigReagentDataChanged = QtCore.Signal(object)  # self
    sigReagentRenamed = QtCore.Signal(object, object, object)  # self, oldname, newname
    
    def __init__(self, db):
        QtCore.QObject.__init__(self)
        self.db = db
        self._dtype = [
            ('group', object),
            ('name', object),
            ('formula', object),
            ('molweight', float),
            ('osmconst', float),
        ] + [(ion, float) for ion in IONS] + [('notes', object)]
        self._null = (None, None, '', 0, 0) + (0,)*len(IONS) + ('',)
        self._data = np.empty(0, dtype=self._dtype)

    def remove(self, name):
        try:
            i = np.argwhere(self._data['name'] == name)[0, 0]
        except IndexError:
            raise KeyError('No reagent named "%s"' % name)
        mask = np.ones(len(self._data), dtype=bool)
        mask[i] = False
        self._data = self._data[mask]

        self.sigReagentListChanged.emit(self)

    def save(self):
        return _saveArray(self._data)
    
    def restore(self, data):
        self._data = _loadArray(data, self._dtype)
        self.sigReagentListChanged.emit(self)
        self.sigReagentDataChanged.emit(self)

    def groups(self):
        return np.unique(self._data['group'])
    
    def names(self):
        return self._data['name'].copy()

    def add(self, name, group, **kwds):
        pos = np.argwhere(self._data['group'] == group)
        if len(pos) == 0:
            pos = len(self._data)
        else:
            pos = pos[-1, 0] + 1
        
        data = np.empty(len(self._data)+1, dtype=self._dtype)
        data[:pos] = self._data[:pos]
        data[pos+1:] = self._data[pos:]
        data[pos] = self._null
        data[pos]['name'] = name
        data[pos]['group'] = group
        for k,v in kwds.items():
            data[pos][k] = v
        self._data = data
        
        self.sigReagentListChanged.emit(self)
    
    def rename(self, n1, n2):
        if n1 == n2:
            return
        if n2 in self._data['name']:
            raise NameError("A reagent named '%s' already exists." % n2)
        ind = self._getIndex(n1)
        self._data[ind]['name'] = n2
        self.db.reagentRenamed(n1, n2)
        self.sigReagentRenamed.emit(self, n1, n2)
        self.sigReagentListChanged.emit(self)
        
    def setData(self, name, item, value):
        ind = self._getIndex(name)
        self._data[ind][item] = value
        self.sigReagentDataChanged.emit(self)

    def __getitem__(self, name):
        if name not in self._data['name']:
            raise NameError("No reagent named '%s'" % name)
        return Reagent(self, name)
    
    def __iter__(self):
        for name in self._data['name']:
            yield self[name]
    
    def getRecArray(self, names):
        inds = []
        for n in names:
            r = np.argwhere(self._data['name'] == n)[:,0]
            if r.shape[0] == 0:
                continue
            inds.append(int(r[0]))

        return self._data[inds]
    
    def _getIndex(self, reagent):
        r = np.argwhere(self._data['name'] == reagent)[:,0]
        if r.shape[0] == 0:
            raise NameError('No reagent named "%s".' % reagent)
        return r[0]
        

class Reagent(object):
    def __init__(self, reagents, name):
        self.reagents = reagents
        self.name = name
        
    def __setitem__(self, item, val):
        if item == 'name':
            self.reagents.rename(self.name, val)
            self.name = val
        else:
            self.reagents.setData(self.name, item, val)

    def __getitem__(self, item):
        ind = self.reagents._getIndex(self.name)
        return self.reagents._data[ind][item]

    @property
    def fields(self):
        dtype = self.reagents._data.dtype
        return OrderedDict([(n, dtype[n]) for n in dtype.names])
    

class Solutions(QtCore.QObject):
    """Collection of grouped Solutions.
    """
    solutionListChanged = QtCore.Signal(object)  # self
    solutionDataChanged = QtCore.Signal(object, object)  # self, solution
    
    def __init__(self, db):
        self.db = db
        QtCore.QObject.__init__(self)
        self._data = []

    def add(self, soln=None, name=None, group=None, signal=True):
        if soln is None:
            soln = Solution(name=name, group=group, db=self.db)
        else:
            soln.db = self.db
        for s in self._data:
            if s.name == soln.name:
                raise NameError('Cannot add solution "%s"; another solution with this name already exists.' % soln.name)
        self._data.append(soln)
        soln._setSolutionList(self)
        soln.sigRenamed.connect(self.solutionRenamed)
        if signal:
            self.solutionListChanged.emit(self)
    
    def solutionRenamed(self, soln, old):
        new = soln.name
        for soln in self._data:
            if soln.compareAgainst == old:
                soln.compareAgainst = new
        self.solutionListChanged.emit(self)
    
    def remove(self, soln):
        self._data.remove(soln)
        self.solutionListChanged.emit(self)
    
    def __getitem__(self, name):
        for sol in self._data:
            if sol.name == name:
                return sol
        raise KeyError(name)

    def __iter__(self):
        for soln in self._data:
            yield soln
    
    def restore(self, data):
        self._data = []
        for d in data:
            sol = Solution(db=self.db)
            sol.restore(d)
            self.add(sol, signal=False)
            #self._data.append(sol)
        self.solutionListChanged.emit(self)
    
    def save(self):
        state = []
        for sol in self._data:
            state.append(sol.save())
        return state

    def recalculate(self, solutions, temperature):
        """Return estimated ion concentrations, osmolarity, and reversal potentials."""
        results = {}
        for soln in solutions:
            ions, osm = soln.recalculate()

            if soln.compareAgainst is None:
                revs = {ion: None for ion in IONS}
            else:
                against = self[soln.compareAgainst].recalculate()[0]
                if soln.type == 'external':
                    external = ions
                    internal = against
                else:
                    external = against
                    internal = ions
                R = 8.31446
                T = temperature + 273.15
                F = 96485.333
                revs = {}
                for ion, z in IONS.items():
                    if internal[ion] == 0 and external[ion] == 0:
                        revs[ion] = None
                    else:
                        revs[ion] = 1000 * ((R * T) / (z * F)) * np.log((external[ion]+1e-6) / (internal[ion]+1e-6))
        
            results[soln.name] = [ions, osm, revs]
            
        return results

    def reagentRenamed(self, old, new):
        for sol in self._data:
            sol.reagentRenamed(old, new)


class Solution(QtCore.QObject):
    """Defines the list of reagents and their concentrations in a solution.
    """
    sigSolutionChanged = QtCore.Signal(object)  # self
    sigRenamed = QtCore.Signal(object, object)  # self, old_name
    
    def __init__(self, name=None, group=None, against=None, db=None):
        QtCore.QObject.__init__(self)
        self.db = db
        self._name = name
        self.group = group
        self.notes = ''
        self.type = 'internal' if group is not None and 'internal' in group.lower() else 'external'
        self.compareAgainst = against
        self._reagents = {}
        
        # empirically determined values:
        self.ionConcentrations = {}
        self.osmolarity = None
        
        self._solutionList = None
        
    @property
    def name(self):
        return self._name
    
    def setName(self, name):
        old = self._name
        if name == old:
            return
        if self._solutionList is not None:
            sl = self._solutionList()
            for s in sl:
                if s.name == name:
                    raise NameError('Cannot rename to "%s"; another solution with this name already exists.' % name)
        self._name = name
        self.sigRenamed.emit(self, old)
        
    def __setitem__(self, name, concentration):
        """Set the concentration of a particular reagent.
        """
        if concentration in (0,  None):
            self._reagents.pop(name, None)
        else:
            self._reagents[name] = concentration
        self.sigSolutionChanged.emit(self)
        
    def __getitem__(self, name):
        """Return the concentration of a reagent, or None if the solution does
        not contain the reagent.
        """
        return self._reagents.get(name, None)
    
    def reagentList(self):
        return list(self._reagents.keys())
    
    @property
    def reagents(self):
        return self._reagents.copy()

    def copy(self):
        soln = Solution()
        soln.restore(self.save())
        return soln
    
    def save(self):
        # Sort reagent list before storing to ensure the order is stable
        # (otherwise diffs become difficult to read)
        reagents = OrderedDict()
        for r in sorted(self._reagents.keys()):
            reagents[r] = self._reagents[r]
            
        return {'name': self.name, 'group': self.group, 'reagents': reagents,
                'type': self.type, 'compareAgainst': self.compareAgainst, 'notes': self.notes}
    
    def restore(self, state):
        self._reagents.clear()
        self._reagents.update(state['reagents'])
        self.group = state['group']
        self.type = state['type']
        self.compareAgainst = state['compareAgainst']
        self.notes = state['notes']
        self.setName(state['name'])
        self.sigSolutionChanged.emit(self)

    def recalculate(self):
        """Calculate ion concentrations and osmolarity.
        """
        reagents = self.db.reagents
        allReagents = reagents.names()
        knownReagents = [r for r in self._reagents.keys() if r in allReagents]
        reagents = reagents.getRecArray(knownReagents)
        concs = np.array([self._reagents[n] for n in reagents['name']])
        ions = {}
        for ion in IONS:
            ions[ion] = np.sum(reagents[ion] * concs)
        
        osm = np.sum(concs * reagents['osmconst'])
        return ions, osm

    def _setSolutionList(self, sl):
        # Just allows solution to ensure that its name is unique when renamed
        self._solutionList = weakref.ref(sl)

    def reagentRenamed(self, old, new):
        changed = False
        if old in self._reagents:
            self._reagents[new] = self._reagents[old]
            del self._reagents[old]
            changed = True
        #if changed:
            #self.sigSolutionChanged.emit(self)


def _saveArray(data):
    return [_recToDict(rec) for rec in data]
    
def _recToDict(rec):
    od = OrderedDict()
    for field in rec.dtype.names:
        if rec.dtype.fields[field][0].names is None:
            od[field] = rec[field]
        else:
            od[field] = _recToDict(rec[field])
    return od
    

def _loadArray(data, dtype):
    arr = np.empty(len(data), dtype=dtype)
    for i,rec in enumerate(data):
        _loadRec(arr[i], rec)
    return arr
        
def _loadRec(arr, rec):
    for field in arr.dtype.names:
        if arr.dtype.fields[field][0].names is None:
            arr[field] = rec[field]
        else:
            _loadRec(arr[field], rec[field])
        

class Recipe(QtCore.QObject):
    """Defines a list of volumes for which reagent masses should be calculated
    for a particular solution.
    """
    sigChanged = QtCore.Signal(object)  # self
    
    def __init__(self, solution=None, volumes=None, notes=None, db=None):
        QtCore.QObject.__init__(self)
        self.db = db
        self._solution = None
        self.volumes = [] if volumes is None else volumes
        self.notes = notes
        if solution is not None:
            self.setSolution(solution)
            
    @property
    def solution(self):
        return self._solution

    def setSolution(self, sol):
        if self._solution is not None:
            self._solution.sigSolutionChanged.disconnect(self.solutionChanged)
        self._solution = sol
        sol.sigSolutionChanged.connect(self.solutionChanged)
        self.solutionChanged()
        
    def solutionChanged(self):
        self.sigChanged.emit(self)

    def save(self):
        return {'solution': self.solution.name, 'volumes': self.volumes, 'notes': self.notes}

    def restore(self, state):
        self.notes = state['notes']
        self.volumes = state['volumes']
        self.setSolution(self.db.solutions[state['solution']])

    def copy(self):
        r = Recipe()
        r.volumes = self.volumes[:]
        r.notes = self.notes
        r.setSolution(self._solution)
        return r


class RecipeSet(QtCore.QObject):
    """Multiple Recipes meant to be displayed together.
    """
    sigRecipeListChanged = QtCore.Signal(object)  # self
    
    def __init__(self, name=None, recipes=None, order=None, stocks=None, db=None):
        QtCore.QObject.__init__(self)
        self.db = db
        self.name = name
        self._recipes = [] if recipes is None else recipes
        self.reagentOrder = [] if order is None else order
        # concentrations of stock solutions per reagent
        self.stocks = {} if stocks is None else stocks  
        self.showMW = False
        self.showConcentration = False

    def add(self, r):
        self._recipes.append(r)
        self.sigRecipeListChanged.emit(self)
        
    def remove(self, r):
        self._recipes.remove(r)
        self.sigRecipeListChanged.emit(self)

    def __iter__(self):
        for r in self._recipes:
            yield r
            
    def __len__(self):
        return len(self._recipes)
        
    def __getitem__(self, i):
        return self._recipes[i]
        
    def save(self):
        recipes = [r.save() for r in self._recipes]
        return {'name': self.name, 'order': self.reagentOrder[:], 'stocks': self.stocks.copy(),
                'showMW': self.showMW, 'showConcentration': self.showConcentration,
                'recipes': recipes} 

    def restore(self, state):
        self.__dict__.update(state)
        self._recipes = []
        for rstate in state['recipes']:
            r = Recipe(db=self.db)
            r.restore(rstate)
            self._recipes.append(r)
        self.sigRecipeListChanged.emit(self)

    def copy(self, name):
        rs = RecipeSet(db=self.db)
        rs.restore(self.save())
        rs.name = name
        rs.recipes = [r.copy() for r in self._recipes]
        return rs
    
    def reagentRenamed(self, old, new):
        if old in self.reagentOrder:
            self.reagentOrder[self.reagentOrder.index(old)] = new
            changed = True
        if old in self.stocks:
            self.stocks[new] = self.stocks[old]
            del self.stocks[old]
            changed = True


class RecipeBook(QtCore.QObject):
    """A simple collection of RecipeSets.
    """
    sigRecipeSetListChanged = QtCore.Signal(object)  # self
    
    def __init__(self, db=None):
        QtCore.QObject.__init__(self)
        self.db = db
        self._recipeSets = []

    def save(self):
        return [r.save() for r in self._recipeSets]

    def add(self, rs):
        self._recipeSets.append(rs)
        rs.db = self.db
        self.sigRecipeSetListChanged.emit(self)

    def remove(self, rs):
        self._recipeSets.remove(rs)
        self.sigRecipeSetListChanged.emit(self)

    def restore(self, state):
        self._recipeSets = []
        for s in state:
            rs = RecipeSet(db=self.db)
            rs.restore(s)
            self._recipeSets.append(rs)
        self.sigRecipeSetListChanged.emit(self)

    def __getitem__(self, i):
        return self._recipeSets[i]

    def __len__(self):
        return len(self._recipeSets)

    def __iter__(self):
        for rs in self._recipeSets:
            yield rs

    def reagentRenamed(self, old, new):
        for rset in self._recipeSets:
            rset.reagentRenamed(old, new)


class SolutionDatabase(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.reagents = Reagents(db=self)
        self.solutions = Solutions(db=self)
        self.recipes = RecipeBook(db=self)
        
    def save(self):
        return {
            'reagents': self.reagents.save(),
            'solutions': self.solutions.save(),
            'recipes': self.recipes.save(),
        }
        
    def restore(self, state):
        self.reagents.restore(state['reagents'])
        self.solutions.restore(state['solutions'])
        self.recipes.restore(state['recipes'])

    def saveFile(self, filename):
        """Save the state of this database to a JSON-formatted file.
        """
        fh, tmpfile = tempfile.mkstemp()
        try:
            try:
                os.close(fh)
                fh = open(tmpfile, 'wb')
                # temporarily override json float encoder
                try:
                    orig = json.encoder.FLOAT_REPR
                    json.encoder.FLOAT_REPR = lambda o: format(np.round(o, 12), '.12g')
                    json.dump(self.save(), fh, indent=2)
                finally:
                    json.encoder.FLOAT_REPR = orig
            finally:
                fh.close()
            os.rename(tmpfile, filename)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(None, "ERROR", "File save failed: " + exc.message)
            if os.path.isfile(tmpfile):
                os.remove(tmpfile)
            raise

    def loadFile(self, filename):
        """Restore the database state from a JSON-formatted file.
        """
        state = json.load(open(filename, 'rb'))
        self.restore(state)
        
    def loadDefault(self):
        deffile = os.path.join(os.path.dirname(__file__), 'default.json')
        self.loadFile(deffile)
        
    def reagentRenamed(self, old, new):
        self.solutions.reagentRenamed(old, new)
        self.recipes.reagentRenamed(old, new)
