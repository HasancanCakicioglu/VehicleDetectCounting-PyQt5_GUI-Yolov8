class overspeed_Profile_Controller:
    def __init__(self):
        overspeed_Profile_Controller.plate = []


    def add_overspeed_Profile_info(self,id,frame,dimension1,dimension2,plate_text):
        is_exist = False
        for dictionary in overspeed_Profile_Controller.plate:
            if dictionary["id"] == id:
                is_exist = True
                dictionary["dimension1"] = dimension1
                dictionary["dimension2"] = dimension2
                dictionary["frame"] = frame
                if plate_text is not None:
                    dictionary["plate_text"] = plate_text
        if plate_text==None:
            plate_text=""

        if is_exist == False:
            overspeed_Profile_Controller.plate.append({"id": id,"frame":frame ,"dimension1":dimension1,"dimension2":dimension2,"plate_text":plate_text})
