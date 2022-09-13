# import os
# import oracledb
# import environ

# def do_ecriture_quitance(post_comptable, annee_budgetaire, compte_debit, compte_credit, num_quitance, montant, libele, journee, agent):

#         dsn_tns = oracledb.makedsn(os.environ.get("CGIB_HOST"), os.environ.get("CGIB_PORT"), service_name=os.environ.get("CGIB_DATABASE_SERVICE")) # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
#         conn = oracledb.connect(user=os.environ.get("CGIB_DATABASE_USER"), password=os.environ.get("CGIB_DATABASE_PASS"), dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

#         sql = '''Insert into "brouillard_cgib" ("id", "POSTE_COMPTABLE", "annee_budgetaire", "JOURNAL", "AUXILIAIRE", "COMPTE", "NUM_PIECE", "CODE_PIECE", "ORDONNATEUR", "SENS_ECRITURE",
#         "MONTANT_ECRITURE", "ECRITURE_LIBELLE", "DATE_ECRITURE", "ORIGINE", "ORIGINE_KEY", "DATE_CREATION", "UTILISATEUR_CREATION", "DATE_MODIFICATION", "UTILISATEUR_MODIFICATION", "num_ecriture", 
#         "num_fiche", "expediteur", "destinataire", "lien_ecriture", "date_echeance", "who_done", "when_done", "statut_ecriture", "cloture", "devise", "montant_debit", "montant_credit",
#         "model", "model_line", 
#         "comptable", "SPECIFICATION_SECONDAIRE", "SPECIFICATION_PRINCIPALE", "REFERENCE_2", "observations") 
         
#         values (:1, :2, :3, 'BT-14', null, :4, :5,'QUITCE','0', :6,
#         :7, :8, :9,'CAISSE','QTTCE-JN',sysdate, :10, sysdate, :10, :1,
#         :11, :10, :10, :12, sysdate, :10, sysdate, 'VALIDE','P','CFA', :13, :14, 
#         null, '0', :10, :10, null,'MAJ', '')'''
        
#         SEQ_num_fiche_prov = None
#         SEQ_lien_ecriture = None
#         SEQ_ECRITURES_brouillard = None
        
        
#         with conn.cursor() as cursor:
#             cursor.execute('select SEQ_num_fiche_prov.Nextval from dual')
#             SEQ_num_fiche_prov = cursor.fetchone()[0]
                
#             cursor.execute('select SEQ_lien_ecriture.Nextval from dual')
#             SEQ_lien_ecriture = cursor.fetchone()[0]

#             cursor.execute('select SEQ_ECRITURES_brouillard.Nextval from dual')
#             SEQ_ECRITURES_brouillard = cursor.fetchone()[0]

#             sens_ecriture = 'D'
#             montant_debit = montant
#             montant_credit = 0

#             p_debit = [
#                 SEQ_ECRITURES_brouillard, #1
#                 post_comptable, #2
#                 annee_budgetaire, #3
#                 compte_debit, #4
#                 num_quitance, #5
#                 sens_ecriture, #6
#                 montant, #7
#                 libele, #8
#                 journee, #9
#                 agent, #10
#                 agent, #10
#                 SEQ_ECRITURES_brouillard, #1
#                 SEQ_num_fiche_prov, #11
#                 agent, #10
#                 agent, #10
                
                
#                 SEQ_lien_ecriture, #12
#                 agent, #10
                
#                 montant_debit, #13
#                 montant_credit, #14
                
#                 agent, #10
#                 agent #10
#             ]
#             cursor.execute(sql, p_debit)




#             cursor.execute('select SEQ_ECRITURES_brouillard.Nextval from dual')
#             SEQ_ECRITURES_brouillard2 = cursor.fetchone()[0]
            
#             sens_ecriture = 'C'
#             montant_debit = 0
#             montant_credit = montant
            
#             p_credit = [
#                 SEQ_ECRITURES_brouillard2, #1
#                 post_comptable, #2
#                 annee_budgetaire, #3
#                 compte_credit, #4
#                 num_quitance, #5
#                 sens_ecriture, #6
#                 montant, #7
#                 libele, #8
#                 journee, #9
#                 agent, #10
#                 agent, #10
#                 SEQ_ECRITURES_brouillard2, #1
#                 SEQ_num_fiche_prov, #11
#                 agent, #10
#                 agent, #10
                
                
#                 SEQ_lien_ecriture, #12
#                 agent, #10
                
#                 montant_debit, #13
#                 montant_credit, #14
                
#                 agent, #10
#                 agent #10
#             ]
#             cursor.execute(sql, p_credit)


#             # commit work
#             conn.commit()