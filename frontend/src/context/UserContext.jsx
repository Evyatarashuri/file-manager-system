import { createContext, useState, useEffect } from "react";
import { auth } from "../utils/firebase";
import { 
  signInWithEmailAndPassword, 
  GoogleAuthProvider, 
  signInWithPopup,
  onAuthStateChanged,
} from "firebase/auth";

export const UserContext = createContext();

export function UserProvider({ children }) {

  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null); // <<< NEW

  // =====================================================
  // AUTH STATE LISTENER – Load user + token
  // =====================================================
  useEffect(() => {
    return onAuthStateChanged(auth, async (firebaseUser) => {
      if (!firebaseUser){
        setUser(null);
        setToken(null);        // reset token when logged out
        return;
      }

      const idToken = await firebaseUser.getIdToken(true);
      const claims = (await firebaseUser.getIdTokenResult()).claims;

      setUser({
        email: firebaseUser.email,
        uid: firebaseUser.uid,
        admin: claims.admin === true
      });

      setToken(idToken);       // <<< STORED + ACCESSIBLE GLOBALLY
      sessionStorage.setItem("auth_token", idToken) // persist across refresh
    });
  }, []);

  // =====================================================
  // LOGIN ADMIN
  // =====================================================
  async function loginAdmin(email,password){
    const result = await signInWithEmailAndPassword(auth,email,password);
    const t = await result.user.getIdToken(true);
    setToken(t);
    return result.user;
  }

  // =====================================================
  // GOOGLE LOGIN
  // =====================================================
  async function loginWithGoogle(){
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    const t = await result.user.getIdToken(true);
    setToken(t);
    return result.user;
  }

  // =====================================================
  function logout(){
    auth.signOut();
    setUser(null);
    setToken(null);
    sessionStorage.removeItem("auth_token");
  }

  // =====================================================
  async function loginUser(email,password){
    const result = await signInWithEmailAndPassword(auth,email,password);
    const t = await result.user.getIdToken(true);
    setToken(t);
    return result.user;
  }

  return (
    <UserContext.Provider value={{
      user,
      token,            // <<< You now expose token to API layer
      loginAdmin,
      loginWithGoogle,
      logout,
      loginUser
    }}>
      {children}
    </UserContext.Provider>
  );
}
