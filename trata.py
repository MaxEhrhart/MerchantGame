# -*- encoding: utf-8 -*-
with open(r"D:\Desktop\python_merchant\equipamentos.csv","r") as f:
    linhas = f.readlines()[1:]
    f.close()

linhas_tratadas = []
for linha in linhas:
    item, materiais = linha.rstrip("\n").split(";")
    materiais = materiais.split("|")
    materiais_formatados = []
    for material in materiais:
        material, quantidade_material = material.rsplit(" ", 1)
        material = quantidade_material.strip("x")+"x " + material
        materiais_formatados.append(material)
    linha = item + ";" + "|".join(materiais_formatados)
    linhas_tratadas.append(linha)
    del linha

with open(r"D:\Desktop\python_merchant\equipamentos_tratados.csv","w") as f:
    f.write("\n".join(linhas_tratadas) + "\n")
    f.flush()
    f.close()
