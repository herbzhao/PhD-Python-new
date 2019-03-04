# import the necessary packages
import cv2
import easygui

class scale_bar_finder_class():
    def __init__(self, image):
        self.image = image
        self.start_point, self.end_point = [(),()]
    
    # user mouse click to obtain the scale bar
    # https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
    def mouse_select_area(self, event, x, y, flags, param):
        ''' a method that capture coordinates of the distance on sample '''
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x,y)
        if event == cv2.EVENT_LBUTTONUP:
            self.end_point = (x,y)

    def draw_scale_bar(self):
        self.original_image = self.image.copy()
        cv2.namedWindow("Draw scale bar and press enter")
        cv2.setMouseCallback("Draw scale bar and press enter", self.mouse_select_area)

        
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow("Draw scale bar and press enter", self.image)
            key = cv2.waitKey(100) & 0xFF
            # draw the rectangle for the user clicked points 
            if self.end_point != ():
                    self.image = self.original_image.copy()
                    cv2.rectangle(self.image, self.start_point, self.end_point, (0, 255, 0), 2)
                    scale_bar_pixel = self.end_point[0] - self.start_point[0]
                    self.start_point, self.end_point = [(),()]

            # if the 'x' or 'esc' key is pressed, break from the loop
            if key == ord("x") or key == 27:
                cv2.destroyWindow('Draw scale bar and press enter')
                break
            
            # if the 'enter'  key is pressed, break from the loop
            if key == 13:
                try:
                    scale_bar_distance = easygui.enterbox("What's the scale bar in real distance?", 'Pixel distance: {}'.format(scale_bar_pixel), '1')
                    scale_bar_distance_per_pixel = float(scale_bar_distance)/float(scale_bar_pixel)
                except:
                    scale_bar_distance_per_pixel = 1
                print('scale bar: {}'.format(scale_bar_distance_per_pixel))
                
                cv2.destroyWindow('Draw scale bar and press enter')
                return scale_bar_distance_per_pixel



if __name__ == "__main__":
    folder_name = r"D:\Dropbox\000 - Inverse opal balls\Correlation analysis" +"\\"
    image_name = 'X4-2min -158'
    image_path = r'{}images\{}.jpg'.format(folder_name, image_name)
    # load the image, clone it for output, and then convert it to grayscale
    image = cv2.imread(image_path)
    scale_bar_finder = scale_bar_finder_class(image)
    scale_bar_distance_per_pixel = scale_bar_finder.draw_scale_bar()