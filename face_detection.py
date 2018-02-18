
import cv2, sys, smtplib, time, base64, socket

DEVICE_NUMBER = 0
IMAGE_FILE_NAME = "cat_detected.jpg"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_last_time = 0

# print(str(encoded_string[len(encoded_string) - 10:len(encoded_string)]))

# Bind the socket to the port
server_address = ('100.64.165.9', 10000)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    print ('connection from', client_address)
    break

face_cascade = cv2.CascadeClassifier('/home/aditya-b/git/haarcascades/haarcascade_frontalcatface.xml')
extended_face_cascade = cv2.CascadeClassifier('/home/aditya-b/git/haarcascades/haarcascade_frontalcatface_extended.xml')

IMAGE_CAPTURE_TIMEOUT = 20
last_time = 0

cap = cv2.VideoCapture(0)
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT

if cap.isOpened():
    ret, frame = cap.read()
else:
    sys.exit(1)
    print("Broke")

while(True):
    # Capture frame-by-frame
    cur_time = time.time()
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # more_faces = extended_face_cascade.detectMultiScale(gray, 1.3, 5)
    # Display the resulting frame
    for (x,y,w,h) in faces:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    if len(faces) > 0 and cur_time - last_time >= IMAGE_CAPTURE_TIMEOUT:
        for (x,y,w,h) in faces:
             cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imwrite(IMAGE_FILE_NAME, frame)
        last_time = cur_time
        with open(IMAGE_FILE_NAME, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print(str(encoded_string[len(encoded_string) - 10:len(encoded_string)]))
        print(sys.getsizeof(encoded_string))
        connection.sendall(encoded_string)
        time.sleep(5)

    cv2.imshow('frame',frame)

    # Encode image from file

    # Receive the data in small chunks and retransmit it
    # data = connection.recv(16)
    # print ('received "%s"' % data)
    # if data:
    #     print ('sending data back to the client')
    # # else:
    #     print ('no more data from', client_address)
    #     break
    #

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up the connection
connection.close()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
