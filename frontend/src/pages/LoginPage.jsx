import { useContext, useEffect, useState } from "react";
import { UserContext } from "../context/UserContext";
import { useNavigate } from "react-router-dom";

export default function LoginPage(){

  const { user, loginAdmin, loginWithGoogle, loginUser } = useContext(UserContext);

  // Fields for manual TEST user login
  const [testEmail,setTestEmail] = useState("");
  const [testPassword,setTestPassword] = useState("");

  // Admin fields
  const [adminEmail,setAdminEmail] = useState("");
  const [adminPassword,setAdminPassword] = useState("");

  const [error,setError] = useState("");
  const navigate = useNavigate();

  useEffect(()=>{
    if(user?.admin) navigate("/admin");
    else if(user) navigate("/upload");
  },[user]);

  return(
    <div style={{textAlign:"center",marginTop:90}}>

      <h1>Login 🔐</h1>

      {/* Google Login */}
      <button 
        onClick={loginWithGoogle}
        style={{padding:"12px 22px",borderRadius:8,margin:30,fontSize:18}}>
        Sign In with Google 🚀
      </button>

      <hr style={{width:250,margin:"40px auto"}}/>


      {/* ================ 🧪 TEST USERS (Manual only) ================= */}
      <h2>Login as Test User 🧪</h2>

      <form onSubmit={async e=>{
        e.preventDefault();
        try{
          await loginUser(testEmail,testPassword);
        }catch{
          setError("Wrong credentials or user not registered in Firebase");
        }
      }}>
        <input 
          placeholder="Test user email"
          value={testEmail} 
          onChange={e=>setTestEmail(e.target.value)}
          style={input}
        />
        <input 
          placeholder="Password" 
          type="password"
          value={testPassword} 
          onChange={e=>setTestPassword(e.target.value)}
          style={input}
        />
        <button type="submit" style={btn}>Login</button>
      </form>

      {error && <p style={{color:"red"}}>{error}</p>}



      {/* =================== ADMIN LOGIN ==================== */}
      <h2 style={{marginTop:40}}>Admin Login 👑</h2>

      <form onSubmit={e=>{
        e.preventDefault();
        loginAdmin(adminEmail,adminPassword);
      }}>

        <input 
          value={adminEmail} 
          onChange={e=>setAdminEmail(e.target.value)}
          type="email" 
          placeholder="Admin email" 
          style={input}
        />

        <input 
          value={adminPassword} 
          onChange={e=>setAdminPassword(e.target.value)}
          type="password" 
          placeholder="Password"
          style={input}
        />

        <button type="submit" style={btn}>Login as Admin 🔥</button>
      </form>
    </div>
  )
}

const input={padding:10,width:260,marginBottom:15,fontSize:16}
const btn={background:"#ffb931",padding:"12px 25px",borderRadius:8,marginTop:10,fontSize:17}
