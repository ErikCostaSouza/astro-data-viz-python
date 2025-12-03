# 🌌 Como Usar: Download de Dados Reais do MAST

## ✅ Tudo Pronto!

Criei 3 arquivos novos para você trabalhar com dados **REAIS** de telescópios:

### 📁 Arquivos Criados

1. **`download_mast_data.py`** (359 linhas)
   - Script principal para baixar dados
   - Suporta Hubble e JWST
   - Com processamento automático

2. **`examples/example4_real_data.py`** (250 linhas)
   - Exemplo completo de uso
   - Demonstra 3 configurações de processamento
   - Compara diferentes técnicas

3. **`MAST_DOWNLOADER_GUIDE.md`**
   - Guia detalhado de uso
   - Lista de alvos recomendados
   - Troubleshooting

---

## 🚀 Começar Agora

### Opção 1: Download Básico (M51)
```bash
python download_mast_data.py
```

### Opção 2: Download + Processamento
```bash
python download_mast_data.py --target "M51" --process
```

### Opção 3: JWST
```bash
python download_mast_data.py --source jwst
```

### Opção 4: Ambos + Processamento
```bash
python download_mast_data.py --source both --process
```

---

## 📊 O Que Vai Acontecer

```
1. Conecta ao MAST (arquivo astronomia da NASA)
   ↓
2. Busca observações por alvo (ex: M51)
   ↓
3. Baixa arquivos FITS reais
   ↓
4. [OPCIONAL] Processa com seu pipeline
   ↓
5. Salva PNG em ./data/processed/
```

---

## 🎯 Alguns Alvos Interessantes

### Galáxias
- **M51** (Whirlpool Galaxy) - Clássica
- **M31** (Andrômeda) - Próxima
- **M87** (Galáxia Messier) - Supermassiva

### Nebulosas
- **NGC 6543** (Eye Nebula) - Bonita
- **NGC 1977** (Running Man) - Emissão
- **M42** (Nebulosa de Orion) - Conhecida

### Campos Profundos
- **Hubble Deep Field** - Famoso
- **GOODS South** - Profundo

---

## 💡 Exemplo Completo

```bash
# 1. Baixar dados de NGC6543 (nebulosa)
python download_mast_data.py --target "NGC 6543" --limit 3

# 2. Processar com o pipeline
python download_mast_data.py --target "NGC 6543" --process

# 3. Ver resultado em ./data/processed/
# (abra os PNG com qualquer visualizador)
```

---

## 🔍 Comparar Diferentes Configurações

```bash
# Cria múltiplas versões processadas
python examples/example4_real_data.py
```

Isso gera 3 versões do mesmo arquivo:
- **config1**: Padrão (Asinh + Hot)
- **config2**: Contraste Alto (Log + Viridis)  
- **config3**: Suave (Sqrt + Cool)

---

## ⚡ Dicas de Performance

### Se download está lento:
```bash
# Reduza quantidade
python download_mast_data.py --limit 1
```

### Se arquivo é muito grande:
```bash
# Tente alvo diferente
python download_mast_data.py --target "M31"
```

### Para processar faster:
```bash
# Sem suavização
python examples/example4_real_data.py
```

---

## 🎓 Próximos Passos

1. ✅ Instale astroquery: `pip install astroquery`
2. ✅ Teste download básico: `python download_mast_data.py`
3. ✅ Baixe com processamento: `python download_mast_data.py --process`
4. ✅ Explore diferentes alvos
5. ✅ Modifique configurações no seu código

---

## 📚 Documentação

Para mais detalhes, veja: **`MAST_DOWNLOADER_GUIDE.md`**

---

## ✨ Resumo

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `download_mast_data.py` | Download via CLI | `python download_mast_data.py` |
| `example4_real_data.py` | Exemplo completo | `python examples/example4_real_data.py` |
| `MAST_DOWNLOADER_GUIDE.md` | Documentação | Abrir em editor |

---

**Está tudo pronto para trabalhar com dados REAIS de telescópios! 🌌**
