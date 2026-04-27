import tkinter as tk
from tkinter import messagebox

def calcular():
    try:
        km = float(entry_km.get())
        valor = float(entry_valor.get())
        consumo = float(entry_consumo.get())
        gasosa = float(entry_gasosa.get())
        
        gasto_comb = (km / consumo) * gasosa
        manutencao = km * 0.15
        lucro = valor - gasto_comb - manutencao
        
        label_resultado.config(text=f"LUCRO REAL: R$ {lucro:.2f}", fg="#00FF00" if lucro > 0 else "red")
    except:
        messagebox.showerror("Erro", "Use apenas números e ponto!")

# Configuração da Janela
janela = tk.Tk()
janela.title("RWV HOLDING - SISTEMA DE GESTÃO")
janela.geometry("400x500")
janela.configure(bg="#1a1a1a")

# Título
tk.Label(janela, text="RWV LOG - CALCULADORA", bg="#1a1a1a", fg="gold", font=("Arial", 14, "bold")).pack(pady=20)

# Campos de entrada
campos = [("Distância (KM)", "entry_km"), ("Valor Bruto (R$)", "entry_valor"), 
          ("Consumo Moto (KM/L)", "entry_consumo"), ("Preço Gasolina (R$)", "entry_gasosa")]

for texto, var_name in campos:
    tk.Label(janela, text=texto, bg="#1a1a1a", fg="white").pack()
    globals()[var_name] = tk.Entry(janela)
    globals()[var_name].pack(pady=5)

# Botão
tk.Button(janela, text="CALCULAR LUCRO", command=calcular, bg="gold", fg="black", font=("Arial", 10, "bold")).pack(pady=20)

# Resultado
label_resultado = tk.Label(janela, text="LUCRO REAL: R$ 0.00", bg="#1a1a1a", fg="white", font=("Arial", 12, "bold"))
label_resultado.pack(pady=20)

janela.mainloop()
