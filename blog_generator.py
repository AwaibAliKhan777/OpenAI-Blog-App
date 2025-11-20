import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
from dotenv import dotenv_values

#Load API key from .env

config = dotenv_values(".env")
client = OpenAI(api_key=config["API_KEY"])


#function to generate blog

def generate_blog():
    topic = topic_entry.get()

    if not topic.strip():
        messagebox.showerror("Error", "Please enter a topic!")
        return
    
    try:
        prompt = f"write a blog on `{topic} with a title and a 3 paragraphs`"

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{"role" : "user" , "content" : prompt}],
            max_tokens=800
        )

        blog_text = response.choices[0].message.content


        #Display in text box

        output_text.delete(1.0,tk.END)
        output_text.insert(tk.END , blog_text)

        #save to file

        with open("blog.txt" , "a",encoding="utf-8") as f:
            f.write(blog_text + "\n\n")

        messagebox.showinfo("Success" , "Blog generated and saved to blog.txt!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


#GUI setup

root = tk.Tk()
root.title("AI BLOG GENERATOR")
root.geometry("700x500")

tk.Label(root,text = "Enter topic :").pack(pady=5)
topic_entry = tk.Entry(root,width =50)
topic_entry.pack(pady = 5)

tk.Button(root, text="Generate Blog" ,  command= generate_blog).pack(pady=10)

output_text = scrolledtext.ScrolledText(root,width=80, height=20)

output_text.pack(pady=10)
root.mainloop()