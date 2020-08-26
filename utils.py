import numpy as np

def Words_extraction(data,input_array,case):
    if case==2:
        actual_array=input_array
        check_2=[]

    if case==3:
        check_2,actual_array=input_array[0],input_array[1]
        save_coordinates=[]

    for i in range(1,len(data['textAnnotations'])):
        x_array=[]
        y_array=[]

        box=data['textAnnotations'][i]['boundingPoly']['vertices']
        x1=None
        x2=None
        y1=None
        y2=None

        for b in range(len(box)):
            try:
                x_array.append(box[b]['x'])
            except:
                pass
            try:
                y_array.append(box[b]['y'])
            except:
                pass
        x_array=np.unique(np.array(x_array))
        y_array=np.unique(np.array(y_array))

        if len(x_array)>1:
            x1=min(x_array)
            x2=max(x_array)
        if len(y_array)>1:
            y1=min(y_array)
            y2=max(y_array)

        if (x1!=None) & (x2!=None)& (y1!=None)& (y2!=None):

            if case==1:
                input_array.append([x1,x2,y1,y2])


            if case==2:
                row_number=actual_array[np.where(np.array(actual_array)==y1)[0][0],1]
                check_2.append([row_number,x1,x2])
                

            if case==3:
                row_number=actual_array[np.where(np.array(actual_array)==y1)[0][0],1]
                #print (x1,x2)
                for gg in range(len(check_2)):
                    if x1>=check_2[gg][0]:
                        if x2<=check_2[gg][1]:
#                            print ([row_number,gg],data['textAnnotations'][i]['description'])
                            save_coordinates.append([[row_number,gg],data['textAnnotations'][i]['description']])
    if case==1:
        return input_array
    if case==2:
        return check_2
    if case==3:
        return save_coordinates
    

def rows_split_estimate(y_threshold,check_):
    unique_y=np.unique(np.array(check_)[:,2])

    for pka in range(10):
        for i in range(1,len(unique_y)):
            if unique_y[i]-unique_y[i-1]<y_threshold:
                unique_y[i-1]=unique_y[i]
    unique_y=(np.unique(unique_y))
    
    actual_array=[]
    for i in np.sort(np.array(check_)[:,2]):
        for g in unique_y:
    #         print(i,g)
            if i<=g:
                actual_array.append([i,np.where(unique_y==g)[0][0]])
                break

    return np.array(actual_array)


def duplicate_removing(old_list):
    new_list=[]
    new_list.append(old_list[0])
    for i in range(1,len(old_list)):
        if old_list[i]==old_list[i-1]:
            pass
        else:
            new_list.append(old_list[i])
    return new_list

def Thresholding_adjacent_boundry_matching(x_threshold,tuple_list):
    for i in range(10):
        for i in range(1,len(tuple_list)):
            if tuple_list[i][0]-tuple_list[i-1][1]<x_threshold:
                tuple_list[i][0]=min(tuple_list[i][0],tuple_list[i-1][0])
                tuple_list[i][1]=max(tuple_list[i][1],tuple_list[i-1][1])
    return tuple_list


def Thresholding_same_boundry_matching(x_threshold,tuple_list):
    for s in range(10):
        for i in range(len(tuple_list)-1):
            if tuple_list[i+1][0]-tuple_list[i][0]<x_threshold:
                tuple_list[i][0]=min(tuple_list[i+1][0],tuple_list[i][0])
                tuple_list[i][1]=max(tuple_list[i+1][1],tuple_list[i][1])
    for s in range(10):
        for i in range(1,len(tuple_list)):
            if tuple_list[i][0]-tuple_list[i-1][0]<x_threshold:
                tuple_list[i][0]=min(tuple_list[i-1][0],tuple_list[i][0])
                tuple_list[i][1]=max(tuple_list[i-1][1],tuple_list[i][1])

    for s in range(10):
        for i in range(len(tuple_list)-1):
            if tuple_list[i+1][1]-tuple_list[i][1]<x_threshold:
                tuple_list[i][0]=min(tuple_list[i+1][0],tuple_list[i][0])
                tuple_list[i][1]=max(tuple_list[i+1][1],tuple_list[i][1])

    for i in range(10):
        for i in range(1,len(tuple_list)):
            if tuple_list[i][1]-tuple_list[i-1][1]<x_threshold:
                tuple_list[i][0]=min(tuple_list[i][0],tuple_list[i-1][0])
                tuple_list[i][1]=max(tuple_list[i][1],tuple_list[i-1][1])
    return tuple_list