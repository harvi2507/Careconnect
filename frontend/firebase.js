// firebase.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyBjPaXv1kgAWpGgkTBkQaPq2rPXLNP3TyA",
  authDomain: "careconnect-97956.firebaseapp.com",
  projectId: "careconnect-97956",
  storageBucket: "areconnect-97956.firebasestorage.app",
  messagingSenderId: "279426077364",
  appId: "1:279426077364:web:c147b1318f1573ff833de1"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
