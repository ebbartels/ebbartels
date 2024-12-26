from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # Your implementation goes here!
    x = np.load(filename)
    mu = np.mean(x, axis = 0)
    
    return x - mu
    #raise NotImplementedError

image = load_and_center_dataset('face_dataset.npy')
np.average(image)


def get_covariance(dataset):
    # Your implementation goes here!
    xT = np.transpose(dataset)
    size_mul = dataset.shape[0] - 1
    return np.dot(xT, dataset) /size_mul
    
    #raise NotImplementedError

covar = get_covariance(image)


def get_eig(S, m):
    # Your implementation goes here!
    eignvalues, eignvectors = eigh(S, subset_by_index=[len(S)-m, len(S)-1])
    return np.diag(np.flip(eignvalues)), np.flip(eignvectors, axis=1)
    
    #raise NotImplementedError

Lambda, U = get_eig(covar, 2)
print(Lambda)


def get_eig_prop(S, prop):
    # Your implementation goes here!
    if prop < 0 or prop > 1:
        return "invalid prop"
    val = np.trace(S) * prop
    eignvalues, eignvectors = eigh(S, subset_by_value= [val, np.inf])
    
    return np.diag(np.flip(eignvalues)), np.flip(eignvectors, axis=1)
            
    
    #raise NotImplementedError

Lambda, U = get_eig_prop(covar, 0.07)
print(Lambda)


def project_image(image, U):
    # Your implementation goes here!
    #U_dot_image = np.dot(U, image)
    proj = np.dot(np.transpose(U), image)
    return np.dot(proj, np.transpose(U))
    
    #U_dot_UT = np.dot(U, np.transpose(U))
    #return np.dot(U_dot_UT, image)
    
    #raise NotImplementedError

def display_image(orig, proj):
    # Your implementation goes here!
    # Please use the format below to ensure grading consistency
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    orig_rehape = orig.reshape(64,64)
    proj_reshape = proj.reshape(64,64)
    
    orig_img = ax1.imshow(orig_rehape, aspect='equal')
    ax1.set_title("Original")
    plt.colorbar(orig_img, ax=ax1)
    
    proj_reshape_img = ax2.imshow(proj_reshape, aspect='equal')
    ax2.set_title("Projection")
    plt.colorbar(proj_reshape_img, ax=ax2)
    
    return fig, ax1, ax2
    #raise NotImplementedError

def perturb_image(image, U, sigma):
    # Your implementation goes here!
    x = np.random.normal(0, sigma, len(image))
    
    comb_proj = project_image(x, U)
    
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    orig_rehape = image.reshape(64,64)
    proj_reshape = comb_proj.reshape(64,64)
    
    orig_img = ax1.imshow(orig_rehape, aspect='equal')
    ax1.set_title("Original")
    plt.colorbar(orig_img, ax=ax1)
    
    proj_reshape_img = ax2.imshow(proj_reshape, aspect='equal')
    ax2.set_title("Perturbed")
    plt.colorbar(proj_reshape_img, ax=ax2)
    
    return fig, ax1, ax2
    #raise NotImplementedError

def combine_image(image1, image2, U, lam):
    # Your implementation goes here!
    
    fig, (ax1, ax2, ax3) = plt.subplots(figsize=(9,3), ncols=3)
    
    combine_list = []
    for i in range(len(image1)):
        combine_list.append(image1[i] * lam + image2[i] * (1-lam))
        
    comb_proj = project_image(np.array(combine_list), U)
        
    image1_rehape = image1.reshape(64,64)
    image2_reshape = image2.reshape(64,64)
    comb_reshape = comb_proj.reshape(64,64)
    
    orig_img1 = ax1.imshow(image1_rehape, aspect='equal')
    ax1.set_title("Image 1")
    plt.colorbar(orig_img1, ax=ax1)
    
    orig_img2 = ax2.imshow(image2_reshape, aspect='equal')
    ax2.set_title("Image 2")
    plt.colorbar(orig_img2, ax=ax2)
    
    comb_reshape_img = ax3.imshow(comb_reshape, aspect='equal')
    ax3.set_title("Comb")
    plt.colorbar(comb_reshape_img, ax=ax3)
    
    return fig, ax1, ax2, ax3

    #raise NotImplementedError
