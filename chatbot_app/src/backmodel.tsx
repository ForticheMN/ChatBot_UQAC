import { useState } from "react";

export default function Chatbot() {
  const [messages, setMessages] = useState<{ text: string; from: "user" | "bot" }[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages([...messages, { text: input, from: "user" }]);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      setMessages((prev) => [...prev, { text: data.reply, from: "bot" }]);
    } catch (error) {
      console.error("Erreur chatbot:", error);
    }

    setInput("");
  };

  return (
    <div className="p-4 w-96 mx-auto">
      <div className="border p-2 h-80 overflow-auto">
        {messages.map((msg, index) => (
          <div key={index} className={`p-1 ${msg.from === "user" ? "text-right" : "text-left"}`}>
            <span className={`px-2 py-1 rounded ${msg.from === "user" ? "bg-blue-500 text-white" : "bg-gray-300"}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <input
        className="border p-2 w-full mt-2"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button className="bg-blue-500 text-white p-2 mt-2 w-full" onClick={sendMessage}>
        Envoyer
      </button>
    </div>
  );
}
