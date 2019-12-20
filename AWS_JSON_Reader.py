import json
import io
import datetime
 
#open the file
input_file = io.open("asrOutput_custom_dict_v2.json")
#write the array
json_array = json.load(input_file)
 
#Buffer the segment count. i.e. the are say 203 segments
iSegmentCount = len(json_array['results']['speaker_labels']['segments'])
 
sOutput = "" # make sure the output string is empty
# Loop through the speaker segments
for iSegmentID in range(0,iSegmentCount - 1):
    #Buffer the item (words) count
    iSegmentItemsCount = (len(json_array['results']['speaker_labels']['segments'][iSegmentID]['items']))
    if iSegmentItemsCount > 0 : #some segments are empty so this guards against this error
        #populate the speaker label and segment ID
        sSpeaker = ((json_array['results']['speaker_labels']['segments'][iSegmentID]['items'][0]['speaker_label']))
        tStartSegment = ((json_array['results']['speaker_labels']['segments'][iSegmentID]['items'][0]['start_time']))
        tEndSegment = ((json_array['results']['speaker_labels']['segments'][iSegmentID]['items'][iSegmentItemsCount-1]['end_time']))
        fStartSegment = float(tStartSegment)
        sMinute = str(int(fStartSegment//60)).zfill(2)
        sSeconds = str(int(fStartSegment%60)).zfill(2)
        sOutput += "\n" + sSpeaker + " - " + sMinute + ":" + sSeconds + "\n"
     
        #Loop the items and, if the are in the time frame, print them
        for iTextItem in json_array['results']['items']:
            if len(iTextItem) > 3 : # this is to catch pronunciation vs punctuation
                #Buffer the variables for times and text
                tStartItem = iTextItem['start_time']
                tEndItem = iTextItem['end_time']
                sText = iTextItem['alternatives'][0]['content']
                sSPACER = " "
            else:
                # a bit hack - appreciate here (as AWS doesn#t put a time stamp on punctuation - time values from the last Item are kept)
                sText = iTextItem['alternatives'][0]['content']
                sSPACER = ""
            if float(tStartItem) >= float(tStartSegment) :
                if float(tEndItem) <= float(tEndSegment) :
                    sOutput += sSPACER + sText
                     
print("###################")
print("JSON Loop completed")
print("###################")   
 
### Write-output
now = datetime.datetime.now()
sFileName = "Output" + now.strftime("%Y%m%d%H%M") + ".txt"
text_file = open(sFileName, "w")
text_file.write(sOutput)
text_file.close()
print("###################")
print("File output written")
print("###################")
