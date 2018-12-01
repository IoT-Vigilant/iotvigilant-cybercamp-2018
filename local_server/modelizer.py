"""
###########################################
Gaussian Mixture Model Selection and train
###########################################

--> Performs iterations with different number of gaussian components
--> Selects the first elbow point on the BIC indicator
--> Returns a gmm best-fit model
--> Args: FreeFlow Data for the
"""

import numpy as np
import itertools
import time

from scipy import linalg
#import matplotlib.pyplot as plt
#import matplotlib as mpl
import numpy

from sklearn import mixture


## TODO:
## Process data from freeflow_stack to use as imput data
## Remember to normalize!!


def model_By_Mac(maclist_stack,freeflow_stack):
    gmm_stack=[]
    mac_gmm_stack=[]
    freeflow_mac_array= []
    # Obtain list of unique MACs
    UniqueMACs= list(set(maclist_stack))
    #Iterate each MAClist to
    for mac in UniqueMACs:
        freeflow_mac_array=[]
        # Search for mac index in the freeflow_stack
        maclist_indexes = [index for index, value in enumerate(maclist_stack) if value == mac]

        for idx in maclist_indexes:
            if freeflow_mac_array==[]:
                freeflow_mac_array=numpy.array([freeflow_stack[idx]])
            else:
                freeflow_mac_array=numpy.vstack([freeflow_mac_array, freeflow_stack[idx]])

        if freeflow_mac_array.shape[0]>=10:
            best_gmm= modeler(freeflow_mac_array)
            gmm_stack.append(best_gmm)
            mac_gmm_stack.append(mac)
    return gmm_stack, mac_gmm_stack

def modeler(freeflow):
    print(__doc__)


    ##############################################################################
    # Example Data generation
    # This phase must be replaced with features extracted from Elasticsearch
    # Data should be inserted through freeflow_stack argument
    ##############################################################################
    # Number of samples per component
    n_samples = 500

    # Generate random sample, two components
    np.random.seed(0)
    C = np.array([[0., -0.1,0.3], [1.7, .4, 0.5]])
    X = np.r_[np.dot(np.random.randn(n_samples, 2), C),
              .7 * np.random.randn(n_samples, 3) + np.array([-6, 3, 5])]


    ###############################################################################
    # Sniffed Data from ES. Last N Features extracted with FreeFlow style
    ###############################################################################

    # -> Imported from
    # -> Number of Features: Top 7
    #         -> Number of source IPs
    #         -> Number of destination IPs
    #         -> Number of packets sent in the time frame selected
    #         -> Number of different protocols used (Whole OSI stack) IPs
    #         -> Number of different ports used (source, destination, UDP & TCP)
    #         -> Max number of TCP sequence (To detect big data transfers)
    #         -> Number of source IPs
    X=freeflow


    # #############################################################################
    # GMM model selection with elapsed time
    ###############################################################################
    ##
    # This code, with minimal variations is based on the scikit-learn.org example
    # https://scikit-learn.org/stable/auto_examples/mixture/plot_gmm_selection.html#sphx-glr-auto-examples-mixture-plot-gmm-selection-py
    ##

    t = time.time()
    n_comp_max= 10

    lowest_bic = np.infty
    bic = []
    last_iteration= False
    n_components_range = range(1, n_comp_max)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = mixture.GaussianMixture(n_components=n_components,
                                          covariance_type=cv_type)
            gmm.fit(X)
            last_bic=gmm.bic(X)
            bic.append(last_bic)


            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm
    #        # Search for the first minimum local on BIC and stop
    #        elif last_bic > lowest_bic and n_components > 1:
    #                break


    bic = np.array(bic)
    # color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue',
    #                               'darkorange'])
    # clf = best_gmm
    # bars = []

    elapsed = time.time() - t
    print('Time dedicated to GMM model selection %.5f seconds' % elapsed)

    print('The model uses %s covariance type' % best_gmm.covariance_type)
    print('and %d components' % best_gmm.n_components)
    print(best_gmm)



# Debugging plots, Only usable for 2D features
    '''
    # Plot the BIC scores
    plt.figure(figsize=(8, 6))
    spl = plt.subplot(2, 1, 1)

    for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
        xpos = np.array(n_components_range) + .2 * (i - 2)
        bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                      (i + 1) * len(n_components_range)],
                            width=.2, color=color))
    plt.xticks(n_components_range)
    plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
    plt.title('BIC score per model')
    xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
        .2 * np.floor(bic.argmin() / len(n_components_range))
    plt.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
    spl.set_xlabel('Number of components')
    spl.legend([b[0] for b in bars], cv_types)


    # Plot the winner
    splot = plt.subplot(2, 1, 2)
    Y_ = clf.predict(X)
    for i, (mean, cov, color) in enumerate(zip(clf.means_, clf.covariances_,
                                               color_iter)):
        v, w = linalg.eigh(cov)
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan2(w[0][1], w[0][0])
        angle = 180. * angle / np.pi  # convert to degrees
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(.5)
        splot.add_artist(ell)


    plt.xticks(())
    plt.yticks(())
    plt.title('Selected GMM: full model, 2 components')
    plt.subplots_adjust(hspace=.35, bottom=.02)
    plt.show()
    '''
    return best_gmm


