#criar diretorio vendas
mkdir vendas 
# copiar arquivo para o diretorio vendas
cp dados_de_vendas.csv vendas
cd vendas/
# criar subdiretorio dentro do diretorio vendas
mkdir backup
#copiar arquivo com o filename da data de execução para o diretorio backup
cd backup/
cp dados_de_vendas.csv dados-`date +%Y%m%d`.csv 
#dentro do diretorio backup renomeie o arquivo criado para backup
cp dados-`date +%Y%m%d`.csv  backup-dados-`date +%Y%m%d`.csv 
#criar relatório.txt dentro da pasta backup que contenha todos esses dados:

# Obter a data atual do sistema operacional
echo $(date "+%Y-%m-%d %H:%M") >data_so.txt
# data do primeiro registro de venda do arquivo
awk -F, 'NR==2 {print $5}' backup-dados-`date +%Y%m%d`.csv > data_p.txt
# data do último registro de venda do arquivo 
tail -n 2 backup-dados-`date +%Y%m%d`.csv | head -n 1 | awk -F ',' '{print $5}' > data_u.txt
#quantidade de produtos diferentes vendidos
cat backup-dados-`date +%Y%m%d`.csv | cut -d',' -f2 | uniq | wc -l > qtd.txt
#10 primeiras linhas do arquivo backup
head -n 10 backup-dados-`date +%Y%m%d`.csv > primeirasL.txt
cat *.txt > resumo.txt
rm data_so.txt data_p.txt data_u.txt qtd.txt primeirasL.txt
#código que copie apenas um intervalo de linhas para outro arquivo
sed -n '1,14p' resumo.txt > relatorio`date +%Y%m%d`.txt
rm resumo.txt
#compactar arquivo
zip backup-dados-`date +%Y%m%d`.zip backup-dados-`date +%Y%m%d`.csv 
rm backup-dados-`date +%Y%m%d`.csv
#voltar um diretório para certificar-se que irá excluir dados de vendas no vendas
cd ../
rm dados_de_vendas.csv
cd ../
#agendar de segunda a quinta














 




