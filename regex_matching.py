# -----------------------------------------------------------------------------
# Filename: regex_matching.py
# Author: Luis Alvarez
# This code takes in a regular expression and
# a directory of interests, recursively searches
# within that directory for all files that contain
# matches to the regular expression and outputs
# a dictionary containing all the files
# with number of times the regular expression
# was matched within each file.

# Import Statements -----------------------------------------------------------
import re
import os
import random
import string
import shutil
import matplotlib.pyplot as plt    

# Function Definitions ----------------------------------------------------------

def search_for_regex_match(root_dir,keyword):
    """ 
    
    Arguments:
    
    root_dir -- root directory in which to begin search
    keyword -- regular expression to match
    
    Returns:
    
    Dictionary of filenames as keys and number of mathced
    occurrences as values.
    
    """
    
    # Helper Functions --------------------------------------------------------    
    
    def walklevel(some_dir, level=1):
        """  
        Choose to list the files 
        in some_dir using the level 
        of choice specified by level 
        argument using generator.
        """
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]
                
    # Code --------------------------------------------------------------------
        
    # Assert root_dir is string type
    assert type(root_dir) == type(''), """"Directory argument is not formatted
    properly."""
            
    # Check if root_dir is not a directory
    if os.path.exists(root_dir) and not os.path.isdir(root_dir):
        raise IOError(root_dir + "is not a directory")
    
    # Assert keyword is regular expression
    assert type(keyword) == type(re.compile('')), """Keyword argument is not 
    a reg expression."""

    # Create result dict
    result = {}
    
    # List all files and directories in the first level
    for root, directories, filenames in walklevel(root_dir,level=1):
        
        # Run through each directory recursively
        for directory in directories:
            matches = search_for_regex_match(root_dir+'/'+directory,keyword)
        
        # Look through each file in root_dir
        for filename in filenames:
            # Create the total path
            total_file_path = os.path.join(root,filename)
            # Open the file for reading
            with open(total_file_path) as f:
                # Store in single string; do not remove newline characters
                data = f.read()
                # Find all matching instances
                list_str = re.findall(keyword,data) 
                # Store number of instances in dict with file path as key
                result[total_file_path] = len(list_str)
                
    # matches will not exist at the lowest level
    # in the recursion tree so only attempt
    # merging when matches have been returned
    try:
        if matches != None:
            dall = {}
            for d in [result,matches]:
                dall.update(d)
            return dall
    # Return result if matches doesn't exist
    except:
        return result
        
def plot_data(data,keyword,dir):
    """
    Plot entries in data
    """
    # Assert data is dictionary type 
    assert type(data) == type({}), "Input data is not dictionary type."
    # Assert keyword is regular expression
    assert type(keyword) == type(re.compile('')), """Keyword argument is not 
    a reg expression."""
    # Instantiate figure
    plt.figure(figsize=(15,12))
    # Use a bar plot with key,value pairs
    plt.bar(range(len(data)),data.values(),align='center',width=0.1)
    plt.xticks(range(len(data)),data.keys(),fontsize=5)
    plt.title('Filenames containing matches of \"%s\" within directory: %s' % (keyword.pattern,dir),
              fontsize=18)
    plt.xlabel('Files',fontsize=12)
    plt.ylabel('Occurrences',fontsize=12)        

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    """ Returns a random combination of characters. """
    return ''.join(random.choice(chars) for _ in range(size))

def create_directory_system(key):
    """ Create a directory system and find all the
    possible matches of the regular expression
    the argument 'key' contains. """        
                
    def create_directory(directory):
        """ Helper function for creating individual 
        directories. """
        # If directory already exists, delete and re-create
        try:
            os.mkdir(directory)
        except:
            shutil.rmtree(directory)
            os.mkdir(directory)
    
    def create_files_and_find_match(path):
        """ Helper function for creating files 
        and finding matches."""
        # Result dictionary
        result = {}
        # Create a random number of files
        file_num = random.randint(3,5)
        for i in xrange(0,file_num):
            # Create the file name
            file_name = id_generator(size=random.randint(4,6))
            # Write a random combination of letters and digits
            with open(path+'/'+file_name+'.txt','w') as f:
                for j in xrange(0,100):
                    f.write(id_generator(size=random.randint(50,100))+'/n')
                f.close()
            
            # Read out and find expression matches, storing in result
            with open(path+'/'+file_name+'.txt','r') as f:
                list_matches = re.findall(key,f.read())
                result[path+'/'+file_name+'.txt'] = len(list_matches)
            f.close()
        return result
    
    
    # Create top directory
    top_dir = id_generator(size=random.randint(4,6))
    create_directory(top_dir)
    
    # Create files in top_dir and find matches
    result_dict = create_files_and_find_match(top_dir)
        
    # Create directories and files in directories within the top directory,
    # finding matches, storing, and updating the result_dict
    for num in xrange(0,random.randint(3,5)):
        dir_name = id_generator(size=random.randint(4,6))
        create_directory(top_dir+'/'+dir_name)
        result_i = create_files_and_find_match(top_dir+'/'+dir_name)
        for d in [result_i]:
            result_dict.update(d)
            
    # Return the name of the top directory and the matches result
    return top_dir, result_dict
        
if __name__ == '__main__':
    # Use your regex of choice
    regex_str = '[a-z0-9]'
    regex = re.compile(regex_str)
    # Create a directory system
    top_dir, result = create_directory_system(regex)
    # Search for matches recursively
    recursive_result = search_for_regex_match(top_dir,regex)
    # Check to see if outputs match
    success = (result == recursive_result)
    if success:
        print "Outputs from recursion match creation result!"
    else:
        print "Outputs from recursion do not match creation result!"
    # Plot recursion result
    plot_data(recursive_result,regex,top_dir); plt.show()
    # Remove directory
    shutil.rmtree(top_dir)
