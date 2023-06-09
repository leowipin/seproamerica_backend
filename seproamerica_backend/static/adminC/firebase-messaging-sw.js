importScripts('https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.0/firebase-messaging-compat.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.

firebase.initializeApp({
    apiKey: "AIzaSyDWEsnR-K7xcEb-VRIfu9bJ8lvCOJMRINo",
    authDomain: "prueba-firebase-3d024.firebaseapp.com",
    databaseURL: '<your-database-URL>',
    appId: "1:278441992033:web:5aec7c0db588cbf53d6f20",
    projectId: "prueba-firebase-3d024",
    storageBucket: "prueba-firebase-3d024.appspot.com",
    messagingSenderId: "278441992033",
    measurementId: "G-JELFJZSFJD"

});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
messaging = firebase.messaging(); 
messaging.onBackgroundMessage((payload) => {
    console.log(
      '[firebase-messaging-sw.js] Received background message ',
      payload
    );
    // Customize notification here
    const notificationTitle = 'Background Message Title';
    const notificationOptions = {
      body: 'Background Message body.',
      icon: '/firebase-logo.png'
    };
  
    self.registration.showNotification(notificationTitle, notificationOptions);
  });