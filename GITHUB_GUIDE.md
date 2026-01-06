# 🚀 Guia Rápido: Subindo o Projeto para o GitHub

## Passo 1: Inicializar o Git (se ainda não foi feito)
```bash
git init
```

## Passo 2: Adicionar todos os arquivos
```bash
git add .
```

## Passo 3: Fazer o primeiro commit
```bash
git commit -m "Initial commit: Projeto Separador de PDFs por Data"
```

## Passo 4: Criar repositório no GitHub
1. Acesse: https://github.com/new
2. Nome do repositório: `separador-de-data`
3. Descrição: "Automação Python para organizar PDFs por data usando OCR"
4. Mantenha como **Público**
5. **NÃO** marque "Initialize with README" (já temos um)
6. Clique em "Create repository"

## Passo 5: Conectar com o repositório remoto
Copie a URL do seu repositório (algo como: https://github.com/seuusuario/separador-de-data.git)

```bash
git remote add origin https://github.com/SEUUSUARIO/separador-de-data.git
git branch -M main
```

## Passo 6: Enviar para o GitHub
```bash
git push -u origin main
```

## ✅ Pronto!
Seu projeto estará disponível em: `https://github.com/SEUUSUARIO/separador-de-data`

---

## 📝 Comandos úteis para futuras atualizações

### Adicionar mudanças
```bash
git add .
git commit -m "Descrição da mudança"
git push
```

### Ver status
```bash
git status
```

### Ver histórico
```bash
git log --oneline
```

---

## 🔧 Dica: Atualizar seu perfil do GitHub no README

Depois de criar o repositório, edite o `README.md` e substitua:
- `[@seuusuario]` pelo seu usuário real do GitHub
- `[Seu Nome]` pelo seu nome no LinkedIn
- URLs de exemplo pelos seus links reais

Depois faça:
```bash
git add README.md
git commit -m "Atualiza links do autor no README"
git push
```
