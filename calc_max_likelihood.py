""" Solves using the max_likelihood_method"""

import numpy as np

import scipy.optimize as optimize

def solve_simplex(func, x0):
    optimal = optimize.minimize(func, x0, method="Nelder-Mead")
    print optimal.message
    
    if not optimal.success == True:
        raise IOError("Minimization failed to find a local minima using the simplex method")
    
    return optimal.x
    

def estimate_new_epsilons(data, data_sets, observables, model):
    
    #observables get useful stuff like value of beta
    beta = model.beta
    number_equilibrium_states = len(data_sets)
    
    #first calculate average value of all observables and associated functions 
    
    expectation_observables = []
    epsilons_functions = []
    ni = []
    current_epsilons = model.get_epsilons()
    h0 = []
    pi = []
    
    Q_function = observables.get_q_function
    
    
    
    for i in data_sets:
        use_data = data[i]
        epsilon_function = model.get_potentials_epsilon(use_data)
        observed = observables.compute_observations(use_data)
        num_in_set = np.shape(use_data)[0]
        ni.append(num_in_set)
        pi.append(num_in_set)
        h0.append(epsilon_function(current_epsilons))
        expectation_observables.append(observed)
        epsilons_functions.append(epsilon_function)
    num_observable = np.shape(observed)[i] ## Calculate the number of observables
    
        
    pi =  np.array(pi).astype(float)
    pi /= np.sum(pi)
    state_prefactors = []
    
    for i in range(number_equilibrium_states):
        state_prefactor = pi[i] * observed[i]##these are the parts that don't depend on the re-weighting   
        state_prefactors.append(state_prefactor)
    
    #then wrap up a funciton that takes only epsilons, and outputs a value for Q
    def Qfunction_epsilon(epsilons):
        #initiate value for observables:
        next_observed = np.zeros(num_observable)
        
        #calculate re-weighting for all terms 
        for i in range(number_equilibrium_states):
            #exp(-beat dH) weighted for this state is:
            next_weight = epsilon_functions[i](epsilon) / h0[i]
            next_observed += next_weight * expectation_observables[i]
        
        
        Q = Q_function(next observed)
        return Q 
        
    #Then run the solver
    new_epsilons = solve_simplex(Qfunction_epsilon, current_epsilons) #find local minima of this current set of epsilons
    
    #then return a new set of epsilons... consider adding a method to the model object to automatically udpate epsilons
    
    return epsilons
    
    
    
    
    
    
    
    
    