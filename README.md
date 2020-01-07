# Smart Medical Prescription System

A smart medical prescription system that uses Finger print authentication (for doctor and pharmacists), and RFID technology for patients
smart health card. The system includes 3 types of users patient, physician and pharmacist. The system stores the patients health details
(which can be updated only by a doctor) and also his past prescriptions (which can be added only by a doctor). When the doctor initially
adds a prescription the checked status of the presctiprion is false and later when the medicine is given by the pharmacist (after he opens
the prescription the status of the prescription is set to true).

This system prevents the patient form acquiring multiple prescriptions for the same disease thereby preventing him from acquring narcotic
drugs illegaly leading to adverse drug effects (ADE) due to drug abuse.

The program depends on the following libraries-     
     **1. pip install django        
       2. pip install django-crispy-forms**
     
     
NOTE: This project also contains code to read from fingerprint sensor and rfid sensor which require nodemcu hardware components which need not be necessary you can edit the code to take input from user instead of rfid or fingerprint sensor.   
