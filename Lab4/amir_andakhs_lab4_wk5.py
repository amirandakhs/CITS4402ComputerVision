import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2
# Amir Andakhs 22839936 Week5 Lab4
# choose the specific type of the filter for edge detection and then click on edge detection 
# or change the threshold to display the edge detected. 

# chagneg the circle radius to detect circles 
# change the slider to detect the perfect size for Iris start from 27 from my experience
# for bicycle 33 is perfect match
class ImageGUI:
   
    def __init__(self, master):
       self.master = master
       self.master.title("Image GUI")
       self.original_image = ""
          
       
       # Create a "Load Image" button
       self.load_button = tk.Button(self.master, text="Load Image", command=self.load_image)
       # using grid to put the items in the righ place padding 5 seems to be good
       self.load_button.grid(row=1, column=0,  padx=5, pady=5) 

       # Create a label to display the chosen image in the righ place
       self.image_label = tk.Label(self.master)
       self.image_label.grid(row=0, column=0, padx=5, pady=5)
       
       # setting up teshold for edge detection with default of 10
       self.edge_detection = tk.IntVar()
       self.kernel_size_scale = tk.Scale(self.master, from_=0, to=255,length=250, orient=tk.HORIZONTAL, label="Threshold for edge detection", variable=self.edge_detection,command=self.slider)
       self.kernel_size_scale.set(10)
       self.kernel_size_scale.grid(row=1, column=2, padx=5, pady=5)
       

       # setting up circle radius with default of 10
       self.circle_detection = tk.IntVar()
       self.sigma_scale = tk.Scale(self.master, from_=0, to=100,length=250, orient=tk.HORIZONTAL, label="Approximate radius for circle detection", variable=self.circle_detection, command= self.radius_slider)
       self.sigma_scale.set(8)
       self.sigma_scale.grid(row=2, column=2, padx=5, pady=5)

        # I choose canny and sobel because I got the best result after filtering
       OPTIONS = ["Canny","Sobel"]

       self.type = tk.StringVar()
       self.type.set(OPTIONS[0])

       self.type_menue = tk.OptionMenu(self.master,self.type, *OPTIONS)
       self.type_menue.grid(row=2, column=1, padx=5, pady=5)

       # Create a "edgeDetection" button
       self.edgeDetection_button = tk.Button(self.master, text="Detect Edges", command=self.edgeDetection)
       self.edgeDetection_button.grid(row=1, column=1, padx=5, pady=5)

       # Create a label to display the filtered image
       self.filtered_label = tk.Label(self.master)
       self.filtered_label.grid(row=0, column=2, padx=5, pady=5)

     

    def load_image(self):
        # Open a file selection dialog box to choose an image file
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        # Load the chosen image using PIL
        self.original_image = Image.open(file_path)
        
        
        # Convert the image to Tkinter format and display it on the left side
        photo = ImageTk.PhotoImage(self.original_image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        
    def edgeDetection(self):
        # Convert the original image to grayscale
        grayscale_image = self.original_image.convert('L')

        # getting the type of filter
        filter_type = self.type.get()
        # getting the threshold
        treshold = self.edge_detection.get()
        
        # using the ratio between 2 and 3 of the other 
        upper_treshold_ratio = 0.5
        
        # make it to gray
        np_image = np.array(grayscale_image)
        
        # Blur the image for better edge detection
        img_blur = cv2.GaussianBlur(np_image, (3,3), 0) 

        edges = img_blur

        if filter_type ==  "Canny":
            edges = cv2.Canny(image=img_blur, threshold1=treshold, threshold2=treshold*upper_treshold_ratio)

            
        elif filter_type ==  "Sobel":
            # Perform x and y derivative
            x_filtered = cv2.convertScaleAbs(cv2.Sobel(src=img_blur, ddepth=cv2.CV_16S, dx=1, dy=0))
            y_filtered = cv2.convertScaleAbs(cv2.Sobel(src=img_blur, ddepth=cv2.CV_16S, dx=1, dy=0))
            filtered=cv2.addWeighted(x_filtered,0.5,y_filtered,0.5,0)
            _,edges=cv2.threshold(filtered,treshold,255,cv2.THRESH_BINARY)

        
            
        # Convert the equalized image back to PIL format
        pil_image = Image.fromarray(edges)

        # display the edge detected image
        photo = ImageTk.PhotoImage(pil_image)

        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo


    def circleDetection(self):
        # Convert the original image to grayscale
        org_image = np.array(self.original_image)
        
        grayscale_image = self.original_image.convert('L')

        # getting the threshold
        treshold = self.edge_detection.get()
        # getting the radius
        radius = self.circle_detection.get()
        # using the ratio between 2 and 3
        upper_treshold_ratio = 0.5
        
        # make it to gray
        np_image = np.array(grayscale_image)
        
        # Blur the image for better edge detection
        img_blur = cv2.GaussianBlur(np_image, (3,3), 0)
        
        # we use the canny as cv2.HoughCircles use the canny as well 
        edges = cv2.Canny(image=img_blur, threshold1=170, threshold2=170 * 0.5)


        #  param2 = 20 because if chose smaller it will consider smaller cirrcle which we don't want
        #  I shortened the radius to chose smaller range of differece
        circles = cv2.HoughCircles(img_blur,cv2.HOUGH_GRADIENT,1,10,param1=160,param2=20,minRadius=radius,maxRadius=radius+5)
        circles = np.uint16(np.around(circles))
        # testing purpose
        print(type(circles))

        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(edges,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(org_image,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.waitKey(0)

        
            
        # Convert the equalized image back to PIL format
        pil_image_original = Image.fromarray(org_image)
        # Convert the equalized image back to PIL format
        pil_image = Image.fromarray(edges)
        
        


        # display the original image again        
        photo_org = ImageTk.PhotoImage(pil_image_original)
        self.image_label.configure(image=photo_org)
        self.image_label.image = photo_org

        # display the edge detected image
        photo = ImageTk.PhotoImage(pil_image)

        self.filtered_label.configure(image=photo)
        self.filtered_label.image = photo


    # these two functions to just make the sliders responsive
    def slider(self, res):
        self.circleDetection()
    def radius_slider(self, res):
        self.circleDetection()
    
  
        
            
if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageGUI(root)
    root.mainloop()
