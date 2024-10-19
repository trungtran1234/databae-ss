"use client"

import React from "react"
import { motion } from "framer-motion"

export default function EnhancedAnimatedBackground() {
    return (
        <div className="fixed inset-0 w-full h-full bg-blue-50 overflow-hidden">
            <svg
                viewBox="0 0 1000 1000"
                xmlns="http://www.w3.org/2000/svg"
                className="w-full h-full"
                preserveAspectRatio="xMidYMid slice"
            >
                {/* Background gradient */}
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style={{ stopColor: "#e0f2fe", stopOpacity: 1 }} />
                        <stop offset="100%" style={{ stopColor: "#bfdbfe", stopOpacity: 1 }} />
                    </linearGradient>
                </defs>
                <rect x="0" y="0" width="100%" height="100%" fill="url(#grad1)" />

                {/* Animated circles */}
                <motion.circle
                    cx="10%"
                    cy="10%"
                    r="50"
                    fill="#93c5fd"
                    initial={{ scale: 1 }}
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 8, ease: "easeInOut" }}
                />
                <motion.circle
                    cx="90%"
                    cy="90%"
                    r="70"
                    fill="#60a5fa"
                    initial={{ scale: 1 }}
                    animate={{ scale: [1, 1.3, 1] }}
                    transition={{ repeat: Infinity, duration: 10, ease: "easeInOut" }}
                />

                {/* Animated paths */}
                <motion.path
                    d="M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z"
                    fill="#5a97ed"
                    initial={{ d: "M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z" }}
                    animate={{
                        d: [
                            "M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z",
                            "M0,300 Q250,200 500,300 T1000,300 L1000,0 L0,0 Z",
                            "M0,300 Q250,50 500,300 T1000,300 L1000,0 L0,0 Z",
                        ],
                    }}
                    transition={{ repeat: Infinity, duration: 20, ease: "easeInOut" }}
                />
                <motion.path
                    d="M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z"
                    fill="#3b82f6"
                    initial={{ d: "M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z" }}
                    animate={{
                        d: [
                            "M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z",
                            "M0,600 Q250,750 500,600 T1000,600 L1000,1000 L0,1000 Z",
                            "M0,600 Q250,450 500,600 T1000,600 L1000,1000 L0,1000 Z",
                        ],
                    }}
                    transition={{ repeat: Infinity, duration: 25, ease: "easeInOut" }}
                />

                {/* Floating shapes */}
                <motion.circle
                    x="100"
                    y="200"
                    width="70"
                    height="50"
                    fill="#2563eb"
                    initial={{ rotate: 0 }}
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
                />
                <motion.polygon
                    points="900,100 950,150 900,200 850,150"
                    fill="#1d4ed8"
                    initial={{ rotate: 0 }}
                    animate={{ rotate: -360 }}
                    transition={{ repeat: Infinity, duration: 30, ease: "linear" }}
                />

                {/* Pulsating overlay */}
                <motion.rect
                    x="35%"
                    y="35%"
                    width="30%"
                    height="30%"
                    fill="rgba(147, 197, 253, 0.3)"
                    initial={{ scale: 1 }}
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 15, ease: "easeInOut" }}
                />
            </svg>
        </div>
    )
}