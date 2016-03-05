""" These set of functions will load in a simple 1-D Langevin data set"""
import numpy as np
from pyfexd.model_loaders import Model_Loader


""" USEFUL FUNCTIONS FOR GETTING DESIRED RESULTS FROM MODEL """

class Langevin(Model_Loader):
    """Object for getting data sets and langevin based stuff from the """
    
    def __init__(self, ini_file_name):
        try:
            from langevin_model.model import langevin_model as lmodel
        except:
            raise IOError("langevin_model package is not installed. Please check path variables or install the relevant package from: https://github.com/TensorDuck/langevin_model")
        
        ##remove .ini suffix
        if ".ini" in ini_file_name[-4:]:
            ini_file_name = ini_file_name[:-4]
        self.model = lmodel(ini_file_name)
        
        #indices = np.arange(0, self.model.number_parameters)
        self.use_params = np.where(self.model.fit_parameters)[0] # get indices corresponding to potentials to use
        self.epsilons = self.model.params[self.use_params]
        self.beta = 1.0
        
    def load_data(self,fname):
        return np.loadtxt(fname)
    
    def get_epsilons(self):
        return self.epsilons
    
    def get_potentials_epsilon(self, data):
        """ Takes a 1-d array, outputs a function(epsilons_list) 
        
        get_potentials_epsilons(self, data) should take as input
        some data that is already properly formatted for the model
        in question. Then, it should calculate a function where
        the epsilons are the independent variables. the function
        is formatted to take a list of epsilons as an input and
        return a float number as its output.
        
        """
        
        constants_list = [] #final list of constant pre factor to each model param epsilon
        
        for i in self.use_params:
            constants_list.append(self.model.potential_functions[i](data))

        
        def hepsilon(epsilons):
            #returns an array for the value of H for each frame, given a set of epsilons.
            total = np.zeros(np.shape(data)[0])
            
            for i in range(np.shape(epsilons)[0]):
                total += epsilons[i]*constants_list[i]
            
            total = np.exp(-1.0 * self.beta * total)
            
            return total
        
        
        
        return hepsilon
    
    
    
