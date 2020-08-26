from PIL import Image, ImageDraw
from optparse import OptionParser
import pandas as pd
import numpy as np
import google_ocr
import utils


parser = OptionParser()

parser.add_option("--image_path", "--ip", dest="Testing_image_path", help="Path to Scan Excel sheet Image")
parser.add_option("--api_path", "--ap", dest="Api_Path", help="Path to Google Ocr Api json file",default="apikey.json")
parser.add_option("--img_save", "--is", dest="Result_Image_Save", help="if you don't want to save result images from ocr then False",default=True)



(options, args) = parser.parse_args()



image_path=options.Testing_image_path
Api_path=options.Api_Path
image_save=options.Result_Image_Save

print ('Loading Google Ocr Results')
data=google_ocr.google_ocr_call(Api_path,image_path)

testing_image=Image.open(image_path)
width,height=testing_image.size


y_threshold=int(height/76)
x_threshold=int(width/70)

check_=[]
check_=utils.Words_extraction(data,check_,case=1)

actual_array=utils.rows_split_estimate(y_threshold,check_)

check_2=utils.Words_extraction(data,actual_array,case=2)

check_2=np.array(check_2)
check_2=check_2[check_2[:,0].argsort()]

check_2=check_2[:,1:3]
check_2=check_2[check_2[:,0].argsort()]

check_2=utils.Thresholding_adjacent_boundry_matching(x_threshold,check_2)

check_3=[]
for i in range(len(check_2)):
    check_3.append([check_2[i][0],check_2[i][1]])
check_2=utils.duplicate_removing(check_3)

check_2=utils.Thresholding_same_boundry_matching(x_threshold,check_2)
check_2=utils.duplicate_removing(check_2)

check_2=utils.Thresholding_same_boundry_matching(x_threshold,check_2)
check_2=utils.duplicate_removing(check_2)

save_coordinates=utils.Words_extraction(data,[check_2,actual_array],case=3)



save_di_cor={}
for i in range(len(save_coordinates)):
    try:
        save_di_cor[str(save_coordinates[i][0][0])+'|'+str(save_coordinates[i][0][1])]=save_di_cor[str(save_coordinates[i][0][0])+'|'+str(save_coordinates[i][0][1])]+' '+save_coordinates[i][1]
    except:
        save_di_cor[str(save_coordinates[i][0][0])+'|'+str(save_coordinates[i][0][1])]=save_coordinates[i][1]

keys_dict=list(save_di_cor.keys())


saving_Arr=[]
for i in range(len(keys_dict)):
    row=int(keys_dict[i].split('|')[0])
    col=int(keys_dict[i].split('|')[1])
    saving_Arr.append([row,col,save_di_cor[keys_dict[i]]])

row_col=[]
for i in range(len(saving_Arr)):
    row_col.append([saving_Arr[i][0],saving_Arr[i][1]])

blankarr=np.zeros([max(np.array(row_col)[:,0])+1,max(np.array(row_col)[:,1])+1])

blankarr[blankarr==0]=None

blankarr=blankarr.astype('object')

for i in range(len(saving_Arr)):
    blankarr[saving_Arr[i][0],saving_Arr[i][1]]=saving_Arr[i][2]

dataf=pd.DataFrame(blankarr)
dataf.to_excel(image_path.replace('images/','Results/').split('.')[-2]+'.xlsx',index=False,header=False)

print('Excel file saved as: ',image_path.replace('images/','Results/').split('.')[-2]+'.xlsx')


if image_save:
    source_img = testing_image.convert("RGBA")

    draw = ImageDraw.Draw(source_img)

    for i in range(0,len(data['textAnnotations'])):
        try:
            box=data['textAnnotations'][i]['boundingPoly']['vertices']

            y1=box[0]['y']
            y2=box[-1]['y']
            x1=box[0]['x']
            x2=box[1]['x']
            draw.rectangle(((x1, y1), (x2, y2)),outline='blue')
        except:
            pass


    source_img.save(image_path.replace('images/','Results/').split('.')[-2]+'_ocr.png')
    print ('Ocr Image save as: ',image_path.replace('images/','Results/').split('.')[-2]+'_ocr.png')
    