importScripts('https://www.gstatic.com/firebasejs/7.16.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.16.1/firebase-messaging.js');
firebase.initializeApp({
    apiKey: "AIzaSyB_hL5iWX0KJLatm3Lrrqv-9qu6RIUzZz0",
    authDomain: "prueba-63695.firebaseapp.com",
    databaseURL: "https://prueba-63695.firebaseio.com",
    projectId: "prueba-63695",
    storageBucket: "prueba-63695.appspot.com",
    messagingSenderId: "44397923925",
    appId: "1:44397923925:web:a304015d46d02b59bdcedc",
    measurementId: "G-GS6NW3RMT5",
    vapidKey: "BNV21GYfyf6yQ2vOhqWIHwc9GuNO0iRsYxzMBiVfHbTMeRQsekEcRbuH3Res0qy3hNN35u-tDnXlj3Bhc_Orhqc"
}
);

const messaging = firebase.messaging();