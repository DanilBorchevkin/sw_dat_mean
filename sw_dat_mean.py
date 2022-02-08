import glob
import os

def dat_file_write(data_list, out_filepath, header=[]):
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)
        
def dat_file_read(in_filepatch, has_header=False):
    read_list = list()
    
    lines = None
    with open(in_filepatch, "r") as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if has_header and idx == 0:
            continue
        
        line_list = list()
        for val in line.split('\t'):
            line_list.append(val.replace("\n", ""))
        read_list.append(line_list)
    
    return read_list 

def dat_data_mean(data_list, mean):
    read_list = list()
           
    return read_list  

def main():
    MEAN = 5      # Change this for mean
    INPUT_PATH_MASK = "./input/*.dat"
    OUTPUT_PATH = "./output"

    print("Script is started")

    files = glob.glob(INPUT_PATH_MASK)
    for filepath in files:
        print("Process >> " + filepath)

        try:
            data_list = dat_file_read(filepath, has_header=True)
            data_list_mean = dat_data_mean(data_list, MEAN)
            dat_file_write(data_list_mean, f"{OUTPUT_PATH}/{os.path.basename(filepath).split('.')[0]}_mean.dat")
    
        except Exception as e:
            print("Cannot process >> ", filepath)
            print("Reason >> " + str(e))
            
        finally:
            print()

    print("Script is finished")

if __name__ == "__main__":
    main()