
importScripts('https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.0/firebase-messaging-compat.js');


// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.

firebase.initializeApp({
    // apiKey: "AIzaSyDWEsnR-K7xcEb-VRIfu9bJ8lvCOJMRINo",
    // authDomain: "prueba-firebase-3d024.firebaseapp.com",
    // databaseURL: '<your-database-URL>',
    // appId: "1:278441992033:web:5aec7c0db588cbf53d6f20",
    // projectId: "prueba-firebase-3d024",
    // storageBucket: "prueba-firebase-3d024.appspot.com",
    // messagingSenderId: "278441992033",
    // measurementId: "G-JELFJZSFJD",

    apiKey: "AIzaSyAX5R-9RJycNyRSeMkXkMu186UKWFVEgU8",
    authDomain: "seproamerica-858ec.firebaseapp.com",
    projectId: "seproamerica-858ec",
    storageBucket: "seproamerica-858ec.appspot.com",
    messagingSenderId: "535172499826",
    appId: "1:535172499826:web:328c4ff587231ea6b875eb",
    measurementId: "G-LPBRPZZQC5",
    vapidKey: "BCGjMbCXbkZhlVNxqDrqmohVTxEGxyo_6YBrLQzZabxdS1HwOOUcg6yhykAPO2vUqE4ng8lhrOS5bHrgjhtOO-c"

});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
messaging = firebase.messaging(); 
messaging.onBackgroundMessage(function (payload) {
  console.log(
    '[firebase-messaging-sw.js] Received background message ',
    payload
  );

  notificationTitle = payload.notification.title;
  notificationOptions = {
    body: payload.notification.body,
    icon: "https://www.seproamerica.com.ec/wp-content/uploads/2019/07/Seproamerica-privada-y-electronica-grande-logo-seguridad-ecuador.png",
  };

 
  return self.registration.showNotification(notificationTitle, notificationOptions);
});



// messaging = firebase.messaging.isSupported() ? firebase.messaging() : null;

// if ('serviceWorker' in navigator) {
//   console.log('Registering service worker...')
//   navigator.serviceWorker.register('firebase-messaging-sw.js')
//     .then(function (registration) {
//       console.log('Service Worker Registered');
//       console.log(registration)
//     })
//     .catch(function (err) {
//       console.log('error', err)
//     });

// };

// messaging.onBackgroundMessage(function (payload) {
//   self.clients.matchAll({
//     type: 'window',
//     includeUncontrolled: true
//   }).then(function (clients) {
//     clients.forEach(function (client) {
//       client.postMessage(payload);
//     });
//   });

// });

// self.addEventListener('push', event => {
//   const promiseChain = isClientFocused()
//     .then((clientIsFocused) => {
//       if (clientIsFocused) {
//         console.log('Don\'t need to show a notification.');
//         return;

//       }

//       // Client isn't focused, we need to show a notification.
//       const messageFrom = event.data.json().data.event;

//       const promiseNotify = registration.getNotifications()
//       .then(notifications => {
//         let currentNotification;
  
//         for (let i = 0; i < notifications.length; i++) {
//           console.log(notifications[i].data)
//           if (notifications[i].data &&
//             notifications[i].data.messageFrom === messageFrom) {
//             currentNotification = notifications[i];
//           }
//         }
  
//         return currentNotification;
//       })
//       .then((currentNotification) => {
//         let notificationTitle;
//         const options = {
//           icon: './assets/img/logo.png'
//         }
  
//         if (currentNotification) {
//           // We have an open notification, let's do something with it.
//           const messageCount = currentNotification.data.newMessageCount + 1;
//           let body = '';
//           switch (messageFrom) {
//             case NotificationEvent.VEHICLE_IMPORTED:
//               body = `${messageCount} vehicles has finished importing.`;
//               break;
//             // create cases if needed  
//           }
//           options.body = body;
//           options.data = {
//             messageFrom: messageFrom,
//             newMessageCount: messageCount
//           };
//           notificationTitle = `New Images`;
  
//           // Remember to close the old notification.
//           currentNotification.close();
//         } else {
//           let body = '';
//           switch (messageFrom) {
//             case NotificationEvent.VEHICLE_IMPORTED:
//               body = 'Vehicle has finished importing.'
//               break;
//             // create cases if needed
//           }
//           options.body = body;
//           options.data = {
//             messageFrom: messageFrom,
//             newMessageCount: 1
//           };
//           notificationTitle = `Catch`;
//         }
  
//         return registration.showNotification(
//           notificationTitle,
//           options
//         );
//       });
//       return promiseNotify
//     });


//   event.waitUntil(promiseChain);
// })

// function isClientFocused() {
//   return clients.matchAll({
//     type: 'window',
//     includeUncontrolled: true
//   }).then((windowClients) => {
//     let clientIsFocused = false;

//     for (let i = 0; i < windowClients.length; i++) {
//       const windowClient = windowClients[i];
//       if (windowClient.focused) {
//         clientIsFocused = true;
//         break;
//       }
//     }

//     return clientIsFocused;
//   });
// }