"use client";

import { useState, useEffect } from "react";
import Image from "next/image";

export default function AdminPage() {
  const [username, setUsername] = useState("Kiko");
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (token) {
      // Very basic verify for MVP
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"}/api/v1/auth/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token })
      })
      .then(res => res.json())
      .then(data => {
        if (data.valid) setIsLoggedIn(true);
      })
      .catch(() => {});
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok && data.token) {
        localStorage.setItem("admin_token", data.token);
        setIsLoggedIn(true);
        setMessage("Logged in successfully.");
      } else {
        setMessage(data.detail || "Login failed");
      }
    } catch (err) {
      setMessage("Network error");
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"}/api/v1/auth/change-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
      });
      const data = await res.json();
      if (res.ok) {
        setMessage("Password changed successfully.");
        setOldPassword("");
        setNewPassword("");
      } else {
        setMessage(data.detail || "Change failed");
      }
    } catch (err) {
      setMessage("Network error");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    setIsLoggedIn(false);
    setMessage("Logged out.");
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-[var(--bg-surface)] border-[4px] border-[var(--border-muted)] shadow-2xl">
      <div className="flex justify-center mb-6">
        <Image src="/kiko.png" alt="Kiko Logo" width={64} height={64} className="object-contain" />
      </div>
      <h1 className="text-2xl font-bold text-center mb-6">Admin Access</h1>
      
      {message && <div className="mb-4 text-center text-[var(--accent-forge)] font-bold">{message}</div>}

      {!isLoggedIn ? (
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-bold mb-1">Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={e => setUsername(e.target.value)}
              className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2 text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1">Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2 text-white"
            />
          </div>
          <button type="submit" className="mt-4 bg-[var(--accent-forge)] text-white p-2 font-bold hover:brightness-110">
            ENTER FORGE
          </button>
        </form>
      ) : (
        <div className="flex flex-col gap-8">
          <p className="text-center font-bold text-green-500">You are in the Forge.</p>
          
          <form onSubmit={handleChangePassword} className="flex flex-col gap-4 border-t border-[var(--border-muted)] pt-6">
            <h2 className="font-bold text-lg">Change Password</h2>
            <div>
              <label className="block text-sm font-bold mb-1">Old Password</label>
              <input 
                type="password" 
                value={oldPassword} 
                onChange={e => setOldPassword(e.target.value)}
                className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2 text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-bold mb-1">New Password</label>
              <input 
                type="password" 
                value={newPassword} 
                onChange={e => setNewPassword(e.target.value)}
                className="w-full bg-[var(--bg-card)] border border-[var(--border-focus)] p-2 text-white"
              />
            </div>
            <button type="submit" className="mt-4 border border-[var(--border-focus)] text-white p-2 font-bold hover:bg-[var(--bg-card)]">
              UPDATE PASSWORD
            </button>
          </form>

          <button onClick={handleLogout} className="text-sm text-neutral-400 hover:text-white underline text-center">
            Log out
          </button>
        </div>
      )}
    </div>
  );
}
