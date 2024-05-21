import serial
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Initialize serial connection
ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Update 'COM3' with your Arduino's port

# Create a CSV file for logging data
csv_file = open('data_log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Sensor Value'])  # Header row

# Initialize lists for plotting
timestamps = []
sensor_values = []

# Initialize plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'bo-')
ax.set_xlabel('Time')
ax.set_ylabel('Sensor Value')
ax.set_title('Real-Time Sensor Data')

# Read and visualize data
try:
    while True:
        data = ser.readline().decode().strip()  # Read data from serial
        if data:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')  # Timestamp
            sensor_value = int(data.split(',')[0])  # Extract sensor value
            timestamps.append(timestamp)
            sensor_values.append(sensor_value)
            
            # Update plot
            line.set_xdata(range(len(timestamps)))
            line.set_ydata(sensor_values)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.001)
            
            # Log data to CSV file
            csv_writer.writerow([timestamp, sensor_value])
except KeyboardInterrupt:
    print("Logging stopped by user.")
    csv_file.close()
    ser.close()
