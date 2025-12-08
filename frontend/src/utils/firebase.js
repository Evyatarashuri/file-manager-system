import { initializeApp } from "firebase/app";
import { 
  getAuth, 
  GoogleAuthProvider,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signOut 
} from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
};

// Initialize
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({ prompt: "select_account" });

// ===== LOGIN METHODS =====

// 1) Login Popup
export const loginWithGooglePopup = async () => {
  const res = await signInWithPopup(auth, googleProvider);
  return await res.user.getIdToken();
};

// 2) Login Redirect
export const loginWithGoogleRedirect = () => signInWithRedirect(auth, googleProvider);

// 3) Resolve Redirect Login
export const resolveRedirectLogin = async () => {
  const result = await getRedirectResult(auth);
  if (!result) return null;
  return await result.user.getIdToken();
};

// Logout
export const logoutFirebase = () => signOut(auth);
