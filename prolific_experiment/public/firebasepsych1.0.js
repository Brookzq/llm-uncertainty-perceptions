// Firebase Psych JavaScript Library v. 1.0
// Author: Mark Steyvers
// to do: 
// save random id / firebase id mapping in database (not readable to anybody)
// update to new function getUrlParameters() {

// The following code uses the modular and functional approach of Firebase version 9
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
import {firebaseConfig} from "./firebaseconfig.js";
import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";

// Initialize App
export const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth( firebaseApp );
const db = getDatabase( firebaseApp );

await signInAnonymously(auth)
  .then(() => {
    // console.log( "Firebase authentication successful...")
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    const msg = "Firebase authentication failed. Errorcode: " + errorCode + " : " + errorMessage;
    //console.error( msg );
    throw( msg );
  });

export async function getUserID() {
  return new Promise((resolve, reject) => {
    onAuthStateChanged(auth, (user) => {
      if (user) {     
        resolve(user.uid);
      } else {
        reject("Firebase user ID not found.");
      }
    });
  });
}

export async function writeRealtimeDatabase( myPath , value ) {
   await set( ref( db, myPath ) , value, { merge: true } )
       .then(() => {
           //console.log( "Write operation successful...")
       })
       .catch((error) => {
           const errorCode = error.code;
           const errorMessage = error.message;
           const msg = "writeRealtimeDatabase( '" + myPath + "' , '" + value + "' ) failed. " + "  Errorcode: " + errorCode + " : " + errorMessage
           //console.error( msg );
           throw( msg );
       });
}