# manual annotated classes
# signature: set_[CLASS-NAME] = set of columns

set_cpfCnpj = set(['cpf_cnpj_proprietario', 'cpf_cnpj_operador', 'cnpj_cpf', 'cpf_cnpj_operador', 'cpf_cnpj_proprietario', 'cpfoucnpjdosancionado', 'nr_cnpj_cpf_empresa', 'num_cpf_cnpj',
	'cpf', 'cpf_segurado', 'cpf_dependente', 'cdigoconvenente', 'nr_cpf_candidato', 'num_cpf', 'num_cpf_entrevistador_fam', 'num_cpf_pessoa', 'num_cpf_pensionista', 'cpf', 'cpf99999999999', 'cpf_1', 'cpf_dependente', 'cpf_instituidor', 'cpf_pensionista', 'cpf_pr_master', 'cpf_segurado', 'cpffavorecido',
	'cnpj', 'cnpj_empresa', 'cnpj_mpmg', 'cnpjcontratado', 'cnpjdosancionado', 'cnpjentidade', 'cnpjparticipante', 'cnpjvencedor', 'idcnpj_4', 'dcod_familiar_fam', 'cdigofavorecido', 'identificacao', 'id_cartorio', 'tipo_valor_completo', 'cartorioid'])

set_tituloEleitor = set(['nr_titulo_eleitoral_candidato', 'ttuloeleitor', 'num_inscricao', 'tituloeleitor', 'tituloeleitordv', 'num_titulo_eleitor_pessoa'])

set_nis = set(["nisfavorecido", 'nisbeneficirio','nisfavorecido', 'num_nis_pessoa_atual', 'pispasep','pis_pasep_dependente'])

set_email = set(["correio_eletronico", "email", "email_1", 'des_email', 'nm_email'])

set_telefone = set(["ddd_telefone_1", "ddd_telefone_2", "telefone", 'tel1', 'tel2', 'telefones', 'celular', 'tel1_13', 'tel2_14',  'nr_telefone_fonte_sancao','num_tel_eleitor', 'num_tel_eleitor_2', 'num_tel_contato_1_fam', 'fax', 'num_ddd_contato_1_fam', 'num_tel_contato_2_fam', 'ddd', 'ddd_12', 'fax_ddd', 'ddd', 'ddd', 'fax_numero'])

# meeting with MPMG: discard this class
#set_identidade = set(["identidade", 'rg_dependente', 'num_identidade_pessoa'])

set_endereco_logradouro = set(["descricao_tipo_logradouro", "logradouro", 'endereo', 'tipologradouro', 'complemento', 'endereco', 'endereo_7', 'logradouro_numero','ds_endereco_fonte_sancao','nom_logradouro', 'num_endereco', 'des_complemento', 'des_endereco','cartorioendereco', 'complemento1', 'nom_localidade_fam', 'nom_tip_logradouro_fam', 'nom_titulo_logradouro_fam', 'nom_logradouro_fam', 'num_logradouro_fam', 'des_complemento_fam', 'des_complemento_adic_fam', 'txt_referencia_local_fam', 'nome_oficial_tipo', 'abreviatura_tipo'])

set_endereco_uf = set(['sg_uf', 'uf_proprietario',"uf", 'uf_operador', 'ufrecebimento', 'cartoriouf',  'siglauf','sg_uf_orgao_sancionador',
                      'cduf', 'ufrgosancionador', 'ctpsuf', 'sg_uf_empresa', 'uf_11', 'uf_unidade_resp', 'ufresidncia',
                      "nm_ue", 'estadoresidncia', 'estadorecebimento','sg_uf_nascimento', 'ufemisso','sig_uf_munic_nasc_pessoa',
                      'sig_uf_escola_memb','sig_uf_ident_pessoa',  'sig_uf_cart_trab_pessoa','uf_exercicio', 'sg_ue'
                      ])

set_endereco_cep = set(["cep", 'cep_9', 'num_cep', 'caixa_postal', 'num_cep_logradouro_fam'])

set_endereco_cidade = set(["nomemunicpio",  'nm_municipio_nascimento',  "municpio", "municipio", 'municpionaturalidade',
                          'nom_municipio',  'nom_munic_nasc', 'cidade',  'nomemunicpiosiafi', 'municpioresidncia',
                          'municpiorecebimento', 'cidade_unidade_resp', 'municpio_10', 'distrito', 'nome_rgo', 
                          'readeabrangncia', 'comarca', 'cartoriocidade', 'agncia', 'nom_munic_escola_memb', 'nom_ibge_munic_nasc_pessoa', 'nom_unidade_territorial_fam',
                          'nom_munic_certid_pessoa'])

set_endereco_bairro = set(["bairro", 'bairro_8', 'cartoriobairro', 'nom_bairro'])

set_nome_pessoa = set(["nome", 'nome_segurando', 'nome_dependente', 'nome_mae_dependente', 
                        'nome_pessoa', 'nome_pessoa_original', 'nm_candidato', 'nm_urna_candidato', 
                        'nm_social_candidato', 'nomeservidor', 'me', 'pai', 'titular', 'substituto',
                        'nome_segurado', 'nome_mae', 'nome_pai', 'nome_pep', 'mae', 'nomebeneficirio',
                        'nomedotitular', 'nomedosubstituto', 'nomedojuiz', 'nome_1', 'nome_pr_master',
                        'nomedotitular_16', 'nomedosubstituto_17', 'nom_eleitor', 'nom_pai', 'nom_mae',
                        'pensionista', 'nom_pai_instituidor', 'nom_mae_instituidor', 'nom_pai_pensionista', 
                        'nom_mae_pensionista', 'nome_instituidor', 'nome_pensionista', 'nome_mae_pensionista', 
                        'nome_mae_instituidor', 'instituidor', 'falecido', 'nom_social_eleitor',
                        'nom_pessoa', 'nom_completo_mae_pessoa', 'nom_completo_pai_pessoa', 'nom_entrevistador_fam',
                        'proprietario', 'outros_proprietarios', 'operador', 'outros_operadores', 
                        'nomeinformadopelorgosancionador', 'cartorionome',  'nomeparticipante', 'favorecido', "nomefavorecido"
                       ])

set_nome_empresa = set(["razao_social", "nome_fantasia",'nomevencedor','empresa',"nomebanco", 'fabricante',
                        'banco', 'abreviaobanco', 'nomefantasia', 'nomefantasiacadastroreceita', 'cartorio', 'nome_empresarial', 'razosocialcadastroreceita', 'nomeoficial', 'nome_estabelecimento', 'nomecontratado',  'nomedocartrio_6', 'nm_empresa_rfb', 'nm_empresa', 'nm_fantasia_empresa', 'nm_empresa_dou','nomeentidade', 'nomeao'])

set_nome_orgao_publico = set(["nomeuo", 'lotacao_oficial_descricao', 'descinst', 'descunid', "nomergosuperior", 
                             "nomergo","nomeug", 'rgosancionador', 'origeminformaes', 'nomergosubordinado',
                              'nomeunidadeoramentria', 'nomergoconcedente', 'nomeconvenente',  'org_lotacao', 'orgsup_lotacao',
                              'uorg_exercicio', 'org_exercicio',  'orgsup_exercicio',  'nm_orgao_sancionador', 'nm_fonte_sancao',
                               'nomeunidadegestora', 'rgosuperior', 'rgo', 'unidadegestora', 'gesto',
                              'orgao_superior_resp', 'orgao_resp', 'unidade_resp','uorg_lotacao', 'org_expedidor',
                              'nom_centro_assist_fam', 'rgoconcedente', 'nomegesto'])

set_metadado = set(['metadata_linha', 'metadata_arquivo', 'metadata_data_ingestao', 'metadata_fonte'])

set_monetaria = set(['valor', 'valororiginaldopagamento', 'valordopagamentoconvertidoprar', 'valorsaque', 'valorparcela', 'valordamulta', 'remuner', 'eventual', 'ir', 'prev', 'rem_pos', 'valorliquidador', 'valorrestosapagarinscritosr', 'valorrestosapagarcancelador', 'valorrestosapagarpagosr', 'val_pag_efet', 'vr_total_ja_recebido', 'valorapostilamento', 'valorlanamentoemr', 'valordescontoemr', 'valorjurosemr', 'valordeduoemr', 'valoracrscimoemr', 'valorliberado', 'valorrecebido', 'valorpagor', 'valorrestosapagarinscritosr', 'valorrestosapagarcancelador', 'valorrestosapagarpagosr', 'valoremr', 'valor', 'valorparcela', 'remuneraobsicabrutar', 'remuneraobsicabrutau', 'abatetetor', 'abatetetou', 'gratificaonatalinar', 'gratificaonatalinau', 'abatetetodagratificaonatalinar', 'abatetetodagratificaonatalinau', 'friasr', 'friasu', 'outrasremuneraeseventuaisr', 'outrasremuneraeseventuaisu', 'irrfr', 'irrfu', 'pssrpgsr', 'pssrpgsu', 'demaisdeduesr', 'demaisdeduesu', 'pensomilitarr', 'pensomilitaru', 'fundodesader', 'fundodesadeu', 'taxadeocupaoimvelfuncionalr', 'taxadeocupaoimvelfuncionalu', 'remuneraoapsdeduesobrigatriasr', 'remuneraoapsdeduesobrigatriasu', 'verbasindenizatriasregistradasemsistemasdepessoalcivilr', 'verbasindenizatriasregistradasemsistemasdepessoalcivilu', 'verbasindenizatriasregistradasemsistemasdepessoalmilitarr', 'verbasindenizatriasregistradasemsistemasdepessoalmilitaru', 'verbasindenizatriasprogramadesligamentovoluntriomp7922017r', 'verbasindenizatriasprogramadesligamentovoluntriomp7922017u', 'totaldeverbasindenizatriasr', 'totaldeverbasindenizatriasu', 'remuneraobsicabrutar', 'remuneraobsicabrutau', 'abatetetor', 'abatetetou', 'gratificaonatalinar', 'gratificaonatalinau', 'abatetetodagratificaonatalinar', 'abatetetodagratificaonatalinau', 'friasr', 'friasu', 'outrasremuneraeseventuaisr', 'outrasremuneraeseventuaisu', 'irrfr', 'irrfu', 'pssrpgsr', 'pssrpgsu', 'demaisdeduesr', 'demaisdeduesu', 'pensomilitarr', 'pensomilitaru', 'fundodesader', 'fundodesadeu', 'taxadeocupaoimvelfuncionalr', 'taxadeocupaoimvelfuncionalu', 'remuneraoapsdeduesobrigatriasr', 'remuneraoapsdeduesobrigatriasu', 'verbasindenizatriasregistradasemsistemasdepessoalcivilr', 'verbasindenizatriasregistradasemsistemasdepessoalcivilu', 'verbasindenizatriasregistradasemsistemasdepessoalmilitarr', 'verbasindenizatriasregistradasemsistemasdepessoalmilitaru', 'verbasindenizatriasprogramadesligamentovoluntriomp7922017r', 'verbasindenizatriasprogramadesligamentovoluntriomp7922017u', 'totaldeverbasindenizatriasr', 'totaldeverbasindenizatriasu', 'valorparcela', 'valortransferido', 'oramentoinicialr', 'oramentoatualizador', 'oramentorealizador', 'valoritem', 'valor', 'valorlicitao', 'valorparcela', 'valorbenefcio', 'valorparcela', 'valoritem', 'valorconvnio', 'valorliberado', 'valorcontrapartida', 'valorltimaliberao', 'val_pag_efet', 'vr_total_ja_recebido', 'valordopagamentoemr', 'valorprecatorioemr', 'valoritem', 'valorunitrio', 'valortotal', 'valorempenhador', 'valorrestosapagarpagosr', 'valor_remuneracao', 'valorinicialcompra', 'valorfinalcompra', 'valorutilizadonaconverso', 'valorlicitao', 'valorliquidador', 'valorpagor', 'valorrestosapagarinscritosr', 'valorrestosapagarcancelador'])

set_dataTempo = set(['datasaque', 'datanaturalizao', 'data_inicio', 'data_termino_dependencia', 'ano', 'datafimefetiva', 'mesano', 'data_inicio_depedencia', 'datanasc', 'data_fim_exerccio', 'datadeinstalao', 'ano_arquivo', 'dt_inscricao', 'dataregistro_19', 'datadotrnsitoemjulgado', 'ltimaatualizao', 'dt_validade_contrato', 'dt_eleicao', 'dat_nascimento', 'datacompleta', 'datapublicaodou', 'dataemisso', 'data_situacao', 'dt_inicio_participacao', 'mes_ano_referencia', 'data_fim_carncia', 'dtcriacao_empresa', 'dataresultadocompra', 'data_nasc_pensionista', 'dt_situacao', 'data_termino_afastamento', 'datafimprevista', 'datafalecimentodesaparecimento', 'data_nasc_instituidor', 'ano_eleicao', 'data_obito_inst', 'datafinalvigncia', 'dtinicio', 'dt_nascimento', 'data_incio_exerccio', 'ano_fab', 'datadeincluso', 'data_inicio_atividade', 'data_inicio_dependencia', 'dt_geracao', 'dataassinaturacontrato', 'data_nascimento_pensionista', 'datacriao', 'data_inicio_pensao', 'dtfim', 'datainciosano', 'dtregistro', 'anoms', 'anomsreferncia', 'data_diploma_ingresso_servicopublico', 'data_ingresso_orgao', 'dtcredenciamento', 'dataltimaliberao', 'data_ultimo_receb_pensao', 'data_fim_pensao', 'data_nascimento', 'datafinalsano', 'ano_mes_referencia', 'data_inicio_inscricao', 'dataemissoob', 'datainciovigncia', 'anomscompetncia', 'datadefimdoacordo', 'datafimvigncia', 'mes_referencia', 'data_nascimento_dependente', 'data_obito', 'dataadm', 'data', 'dtultima_alteracao', 'dataorigeminformaes', 'dataabertura', 'dataincio', 'data_ingresso_cargofuncao', 'datadeinciodoacordo', 'datapublicao', 'anochegadabrasil', 'data_inicio_afastamento', 'anoemsdolanamento', 'data_inicio_receb_pensao', 'data_admissao', 'obito', 'dta_emissao_ident_pessoa', 'data_inicio_atividade', 'data_desligamento', 'data_situacao_cadastral', 'dta_nasc_pessoa', 'dat_atual_fam', 'hora', 'dta_entrevista_fam', 'dt_origem_informacao', 'nascimentodata', 'dta_obito', 'dt_inicio_sancao', 'dta_lavratura', 'dta_nasc'])

set_cnsCartorio = set(['cns'])

set_corRaca = set(['ds_cor_raca'])

set_genero = set(['sexo', 'codsexo', 'ds_genero', 'ds_genero', 'ds_genero', 'sexo', 'codsexo', 'des_sexo', 'ds_genero'])

def getAnnotatedColumns():
	column_class = dict()
	list_sets = [i for i in globals() if i.startswith("set_")]
	for i in list_sets:
		cl = i[i.index("_")+1:]
		for j in globals()[i]:
			column_class[j] = cl
	return column_class

def getAnnotatedColumn(column):
	if "set_"+column in globals():
		return globals()["set_"+column]
	return []

