## Classes já definidas
set_email = set(["correio_eletronico", "email", "email_1", 'des_email', 'nm_email'])

set_titulo_eleitor = set(['nr_titulo_eleitoral_candidato', 'ttuloeleitor', 'num_inscricao', 'tituloeleitor', 
                          'tituloeleitordv', #So tem o digito verificador
                          'num_titulo_eleitor_pessoa',
                         ])

set_nis = set(["nisfavorecido", 'nisbeneficirio','nisfavorecido', 'num_nis_pessoa_atual',
               'pispasep','pis_pasep_dependente', "cod_eas_fam"]) #num_benef_inss
set_cpf_cnpj = set(["cnpj", "cpf", "cpf_cnpj_proprietario", 'cpf_cnpj_operador', 'cpf_segurado', 'cpf_dependente', 
                   'cartorioid','cdigoconvenente','cdigofavorecido','cnpj','cnpj_cpf','cnpj_empresa','cnpj_mpmg','cnpjcontratado','cnpjdosancionado','cnpjentidade','cnpjparticipante','cnpjvencedor','cpf','cpf99999999999','cpf_1','cpf_cnpj_operador','cpf_cnpj_proprietario','cpf_dependente','cpf_instituidor','cpf_pensionista','cpf_pr_master','cpf_segurado','cpffavorecido','cpfoucnpjdosancionado',
                   'nr_cnpj_cpf_empresa','nr_cpf_candidato','num_cpf','num_cpf_cnpj','num_cpf_entrevistador_fam','num_cpf_pensionista','num_cpf_pessoa',
                   'tipo_valor', 'tipo_valor_completo',
                   'inscricaoestadual', 'nire', 'inscricaoestadualmatriz', 'inscricaoestadualpr', #eu acho que eh - CONFERIR
                   'id_cartorio', 'idcnpj_4', "id_cartorio", 'dcod_familiar_fam',])


set_rg = set(["identidade", 'rg_dependente', 'num_identidade_pessoa',])
set_telefone = set(["ddd_telefone_1", "ddd_telefone_2", "telefone", 'fax', 'tel1', 'tel2', 'telefones', 
                    'celular', 'tel1_13', 'tel2_14',  'fax_numero',
                    'nr_telefone_fonte_sancao','num_tel_eleitor', 'num_tel_eleitor_2', 'ddd_fax',
                   'ddd_12', 'fax_ddd', 'ddd', #So tem DDD
                    'num_ddd_contato_1_fam', 'num_tel_contato_1_fam', 'num_ddd_contato_2_fam',
                   ])
#Endereco
set_endereco_logradouro_completos_edemais = set([
                    "descricao_tipo_logradouro", "logradouro", 'endereo', 'tipologradouro', 'complemento',   
                    'endereco', 'endereo_7', 'logradouro_numero','ds_endereco_fonte_sancao','nom_logradouro', 
                    'num_endereco', 'des_complemento', 'des_endereco','cartorioendereco', 'complemento1',
                    'nom_localidade_fam', 'nom_tip_logradouro_fam', 'nom_titulo_logradouro_fam', 'nom_logradouro_fam', 'num_logradouro_fam', 'des_complemento_fam', 'des_complemento_adic_fam',    
    
                    ])
set_endereco_uf = set(['sg_uf', 'uf_proprietario',"uf", 'uf_operador', 'ufrecebimento', 'cartoriouf',  'siglauf','sg_uf_orgao_sancionador',
                      'cduf', 'ufrgosancionador', 'ctpsuf', 'sg_uf_empresa', 'uf_11', 'uf_unidade_resp', 'ufresidncia',
                      "nm_ue", 'estadoresidncia', 'estadorecebimento','sg_uf_nascimento', 'ufemisso','sig_uf_munic_nasc_pessoa',
                      'sig_uf_escola_memb','sig_uf_ident_pessoa',  'sig_uf_cart_trab_pessoa',
                      ])
set_endereco_cep = set(["cep", 'cep_9', 'num_cep', 'caixa_postal', 'num_cep_logradouro_fam' ])
set_endereco_cidade = set(["nomemunicpio",  'nm_municipio_nascimento',  "municpio", "municipio", 'municpionaturalidade',
                          'nom_municipio',  'nom_munic_nasc', 'cidade',  'nomemunicpiosiafi', 'municpioresidncia',
                          'municpiorecebimento', 'cidade_unidade_resp', 'municpio_10', 'distrito', 'nome_rgo', 
                          'readeabrangncia', 'comarca', 'cartoriocidade', 'agncia', 'nom_munic_escola_memb', 'nom_ibge_munic_nasc_pessoa', 'nom_unidade_territorial_fam',
                          'nom_munic_certid_pessoa',])
set_endereco_bairro = set(["bairro", 'bairro_8', 'cartoriobairro', 'nom_bairro',  ])
# funcional
set_matricula_funcional = set(["masp", "id_servidor_portal", 'matricula'])


set_nome_pessoal = set(["nome", 'nome_segurando', 'nome_dependente', 'nome_mae_dependente', 
                        'nome_pessoa', 'nome_pessoa_original', 'nm_candidato', 'nm_urna_candidato', 
                        'nm_social_candidato', 'nomeservidor', 'me', 'pai', 'titular', 'substituto',
                        'nome_segurado', 'nome_mae', 'nome_pai', 'nome_pep', 'mae', 'nomebeneficirio',
                        'nomedotitular', 'nomedosubstituto', 'nomedojuiz', 'nome_1', 'nome_pr_master',
                        'nomedotitular_16', 'nomedosubstituto_17', 'nom_eleitor', 'nom_pai', 'nom_mae',
                        'pensionista', 'nom_pai_instituidor', 'nom_mae_instituidor', 'nom_pai_pensionista', 
                        'nom_mae_pensionista', 'nome_instituidor', 'nome_pensionista', 'nome_mae_pensionista', 
                        'nome_mae_instituidor', 'instituidor', 'falecido', 'nom_social_eleitor',
                        'nom_pessoa', 'nom_completo_mae_pessoa', 'nom_completo_pai_pessoa', 'nom_entrevistador_fam',           
                        
                       ])
set_nome_empresa = set(["razao_social", "nome_fantasia",'nomevencedor','empresa',"nomebanco", 'fabricante',
                        'banco', 'abreviaobanco',])
set_nome_orgao_publico = set(["nomeuo", 'lotacao_oficial_descricao', 'descinst', 'descunid', "nomergosuperior", 
                             "nomergo","nomeug", 'rgoexpedidor', 'rgosancionador', 'origeminformaes', 'nomergosubordinado',
                              'nomeunidadeoramentria', 'nomergoconcedente', 'nomeconvenente',  'org_lotacao', 'orgsup_lotacao',
                              'uorg_exercicio', 'org_exercicio',  'orgsup_exercicio',  'nm_orgao_sancionador', 'nm_fonte_sancao',
                               'nomeunidadegestora', 'rgosuperior', 'rgo', 'unidadegestora', 'gesto',
                              'orgao_superior_resp', 'orgao_resp', 'unidade_resp','uorg_lotacao', 'org_expedidor',
                              'sig_orgao_emissor_pessoa','nom_centro_assist_fam', 
                             ])

set_nome = set(['proprietario', 'outros_proprietarios', 
               'operador', 'outros_operadores', 
                 'nomeinformadopelorgosancionador', 'razosocialcadastroreceita', 'nomefantasiacadastroreceita',
               'cartorio', 'nome_empresarial',
                'nomeoficial', 'nomefantasia', 'nome_estabelecimento', 
                 'nomecontratado',  'nomedocartrio_6', 
                'nm_empresa_rfb', 'nm_empresa', 'nm_fantasia_empresa', 'nm_empresa_dou', 'nomegesto',
                'nomeentidade', 'rgoconcedente', 'cartorionome',  'nomeparticipante', 'favorecido', "nomefavorecido",
               ])