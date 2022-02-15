import glob
import os

def dat_file_write(data_list, out_filepath, header=None):
    write_list = []
    
    if header != None:
        data_list.insert(0, header)

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
    try:
        with open(in_filepatch, "r", encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(in_filepatch, 'r', encoding='utf-16') as f:
            lines = f.readlines()
        
    for idx, line in enumerate(lines):
        if has_header and idx == 0:
            continue
        
        line_list = list()
        for val in line.split('\t'):
            line_list.append(val.replace("\n", ""))
        read_list.append(line_list)
    
    return read_list 

def dat_data_mean(data_list, lat_start, lat_stop, lat_step):
    mean_list = list()
    
    bottom = lat_start
    top = lat_start + lat_step
    
    slice = list()
    slice.extend([0, 0])
    val_counter = 0
    
    slice = list()
    slice.extend([0, 0])
    val_counter = 0
    for record in data_list:
        lat = float(record[0])
        on2 = float(record[1])
        
        if (lat < lat_start) or (lat > lat_stop):
            continue
               
        if (lat < bottom) or (lat > top): 
            cycle_counter = 0                     
            while True:
                #print(f'Out of range [{bottom}:{top}]. Increase the range by <{lat_step}> for pair <{lat}>:<{on2}>')
                slice[0] = (bottom + top) / 2
                if val_counter != 0:
                    slice[1] = slice[1] / val_counter
                mean_list.append(slice)
                
                slice = list()
                slice.extend([0, 0])
                val_counter = 0
                
                bottom = top
                top = bottom + lat_step
                if top > lat_stop:
                    bottom = lat_start
                    top = lat_start + lat_step
                    
                if (lat >= bottom) and (lat <= top):
                    break
                
                cycle_counter += 1
                if cycle_counter > 128:
                    raise Exception('Seems code stuck. Consult with developer')
        
        # Add value to range
        if (lat >= bottom) and (lat <= top):
            val_counter += 1
            slice[1] += on2
        else:
            # Just to be on the safe side
            raise Exception("Lat is outside of range")
    
    # Note previous algorithm lost the last slice
    # Add last slice
    slice[0] = (bottom + top) / 2
    if val_counter != 0:
        slice[1] = slice[1] / val_counter
    mean_list.append(slice)
    
    return mean_list  

def main():
    LAT_START = -90
    LAT_STOP = 90
    LAT_STEP = 5
    INPUT_PATH_MASK = "./input/*.dat"
    OUTPUT_PATH = "./output"

    print("Script is started")

    files = glob.glob(INPUT_PATH_MASK)
    for filepath in files:
        print("Process >> " + filepath)

        try:
            data_list = dat_file_read(filepath, has_header=True)
            data_list_mean = dat_data_mean(data_list, LAT_START, LAT_STOP, LAT_STEP)
            dat_file_write(data_list_mean, f"{OUTPUT_PATH}/{os.path.basename(filepath).split('.')[0]}_mean.dat")
        except Exception as e:
            print("Cannot process >> ", filepath)
            print("Reason >> " + str(e))
            
        finally:
            print()


    print("Script is finished")

if __name__ == "__main__":
    main()