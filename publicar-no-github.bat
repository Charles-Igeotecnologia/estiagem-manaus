@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set LOG=%~dp0publicar.log
echo. > "%LOG%"
echo ============================================================ >> "%LOG%"
echo   EXECUCAO EM %date% %time% >> "%LOG%"
echo   Pasta: %cd% >> "%LOG%"
echo ============================================================ >> "%LOG%"

echo ============================================================
echo   PUBLICAR ALTERACOES NO GITHUB - PROJETO 360
echo ============================================================
echo.
echo Pasta: %cd%
echo (Tudo tambem esta sendo salvo em publicar.log nesta pasta - arquivo ignorado pelo git)
echo.

echo [0/4] Verificando se o Git esta instalado e acessivel...
git --version >> "%LOG%" 2>&1
git --version
if errorlevel 1 (
    echo.
    echo ERRO: o comando "git" nao foi encontrado. Instale o Git para Windows e tente de novo.
    echo ERRO: git nao encontrado >> "%LOG%"
    goto :fim
)

echo.
echo [1/4] Baixando alteracoes mais recentes do GitHub (git pull)...
git pull origin main >> "%LOG%" 2>&1
git pull origin main
if errorlevel 1 (
    echo.
    echo ERRO no "git pull". Veja publicar.log e mande para o Claude.
    goto :fim
)

echo.
echo [2/4] Verificando se ha arquivos em conflito nao resolvido...
git diff --name-only --diff-filter=U > "%TEMP%\conflitos_projeto360.txt"
for %%A in ("%TEMP%\conflitos_projeto360.txt") do set TAMANHO=%%~zA
if not "!TAMANHO!"=="0" (
    echo.
    echo ATENCAO: existem arquivos em conflito de merge. NAO prosseguindo automaticamente.
    type "%TEMP%\conflitos_projeto360.txt" >> "%LOG%"
    type "%TEMP%\conflitos_projeto360.txt"
    echo.
    echo Mande o publicar.log para o Claude antes de tentar de novo.
    del "%TEMP%\conflitos_projeto360.txt" 2>nul
    goto :fim
)
del "%TEMP%\conflitos_projeto360.txt" 2>nul

echo.
echo [2b/4] Mostrando TODAS as alteracoes pendentes na pasta (inclusive de outras pessoas/IAs)...
git status --short >> "%LOG%" 2>&1
git status --short
echo.
echo ATENCAO: este script so vai commitar os arquivos listados abaixo (lista fixa definida pelo Claude).
echo Qualquer outra alteracao pendente (ex: de outra sessao/IA) NAO sera commitada nem enviada por este script.
echo.

echo [3/4] Preparando commit (apenas dos arquivos que o Claude editou nesta rodada)...
rem >>> O Claude atualiza a lista de arquivos E as linhas de mensagem abaixo antes de pedir para voce rodar este arquivo <<<
set ARQUIVOS=README.md escolas_rurais.geojson index.html pocos publicar-no-github.bat

set SUBJECT=Corrige dashboard, adiciona modulo de pocos e atualiza documentacao
set BODY1=- Corrige sobreposicao dos graficos no dashboard (novo grid dashboard-grid-secondary para os 3 graficos de 2024)
set BODY2=- Substitui a caixa Metricas Comparativas por cartoes de Resumo Historico das Estiagens (2023, 2024, Monitoramento Continuo)
set BODY3=- Corrige formatacao de CEP em escolas_rurais.geojson (QA de dados geoespaciais)
set BODY4=- Documenta no README a decisao de nao integrar novas APIs climaticas e a consolidacao index.html/visao_redesign.html
set BODY5=- Adiciona modulo pocos/ (Web Map Leaflet + Dashboard Chart.js) lendo TABELA POCOS 2026.csv real, com classificacao de cenario de estiagem e cruzamento com escolas_rurais.geojson
set BODY6=- Adiciona publicar-no-github.bat para facilitar pull/commit/push

git add -- %ARQUIVOS% >> "%LOG%" 2>&1
git add -- %ARQUIVOS%
echo.
echo Arquivos que serao enviados (deve bater com a lista ARQUIVOS acima):
git status --short >> "%LOG%" 2>&1
git status --short
echo.
git commit -m "%SUBJECT%" -m "%BODY1%" -m "%BODY2%" -m "%BODY3%" -m "%BODY4%" -m "%BODY5%" -m "%BODY6%" >> "%LOG%" 2>&1
git commit -m "%SUBJECT%" -m "%BODY1%" -m "%BODY2%" -m "%BODY3%" -m "%BODY4%" -m "%BODY5%" -m "%BODY6%"
if errorlevel 1 (
    echo.
    echo Nao havia nada novo para commitar, ou houve um erro no commit. Veja publicar.log.
    goto :fim
)

echo.
echo [4/4] Enviando para o GitHub (git push)...
git push origin main >> "%LOG%" 2>&1
git push origin main
if errorlevel 1 (
    echo.
    echo ERRO no "git push". Veja publicar.log e mande para o Claude se precisar de ajuda.
    goto :fim
)

echo.
echo ============================================================
echo   CONCLUIDO! Alteracoes publicadas no GitHub com sucesso.
echo ============================================================
echo CONCLUIDO COM SUCESSO >> "%LOG%"

:fim
echo.
echo Log completo salvo em: %LOG%
echo Esta janela NAO vai fechar sozinha. Pressione qualquer tecla para fechar.
pause
