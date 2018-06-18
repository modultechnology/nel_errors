# nel_errors



This project contains small scripts that were used for the error analysis work described in:

```tex
@inproceedings{brasoveanu2018lrec,
  author = {Adrian M.P. Bra{\c{s}}oveanu and Giuseppe Rizzo and Philipp Kuntschick and Albert Weichselbraun and Lyndon J.B. Nixon},
  title = {Framing Named Entity Linking Error Types},
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  editor = {Nicoletta Calzolari and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
  publisher = {European Language Resources Association (ELRA)},
  address = {Paris, France},
  isbn = {979-10-95546-00-9},
  language = {english},
  pages = {266-271},
  year = {2018},
  month = {may},
  date = {7-12},
  location = {Miyazaki, Japan},
  url = {http://www.lrec-conf.org/proceedings/lrec2018/summaries/612.html}
}
```

### FOLDERS
* src - source code files
* batch - batch files used for running evaluations
* guideline - annotation guideline
* examples - examples discussed in the paper

### DOCUMENTATION
[Documentation](https://github.com/modultechnology/nel_errors/wiki)

### WORKFLOW

#### Current
0. create runs from the annotators and extract gold standards from NIF (methods: get_annotations, get_dbpedia_type and convert_annotations)
    * run - usually contains the normal results directly in a format similar to TAC-KBP
    * run2 - contains normal results + surfaceForms
1. keep only PER, ORG, LOC from the gold standard and runs
    * Why 3 main types? Types commonly and largely used - motivation? why?
2. Analyze the entities of the GS with notype/type and check if one of them actually belongs to the 3 types that we’re interested in. Hunt for the following: 
    * No type
        * Entities that have no type at all in DBpedia (e.g., basically entities that only have the owl:Thing type - http://dbpedia.org/resource/Kenneth_and_Mamie_Clark)
        * Entities with no triple but which are not redirects (e.g., http://dbpedia.org/resource/Dominion_Textiles)
        * Family names (e.g., http://dbpedia.org/resource/Reuter)
http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=describe+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2FReuter%3E&format=text%2Fhtml&CXML_redir_for_subjs=121&CXML_redir_for_hrefs=&timeout=30000&debug=on 
        * Should i still keep it in the GS? Or we mention that an error exists
        * Redirects (e.g., http://dbpedia.org/resource/Carnival_Cruise_Lines)
    * Annotations in another language (e.g., de.dbpedia.org instead of dbpedia.org URIs) 
        * We keep them because we aim to be transparent to the annotator output.
    * Type
        * Check that the resulting types are correct in both gold standard and automated annotator.
3. run neleval evaluate script
    * use normal runs
    * convert normal runs into the TAC-KBP format by using the converter.py script
    * get the P,R,F1 results for different types of run from the evaluate script
4. run neleval analyze script
    * use the normal results + surfaceForms
5. create superset of all errors - Google Docs
    * mergerun - creates the unified tac - tool output that is ready for merging. Uses same header all the time.
    * create combined run via the sort -u file1 file2 ... filen > combined.csv format
    * combineruns - passes the individual runs of each tool through the combined runs and gets the correct counts for each error
6. preselect only KB and GS errors 
7. Manual annotation of the errors
8. Create tables/analytics with results

#### INTERFACE FOR CLIENTS
* get_annotations - extracts annotations from the results
* get_dbpedia_type - gets dbpedia types for a certain entity (it can use a list of types or an url)
* convert_annotations(folder,run) - converts annotations to a format close to the TAC-KBP evaluation format

#### CURENT CORPORA

##### ENGLISH
* Reuters128 -> OK
* KORE50
##### GERMAN
* RBB150 (RBB)
##### FRENCH
##### SPANISH



#### CURRENT ANNOTATORS
* AIDA 
* Spotlight
* Babelnet
* Recognyze (German)

#### GERBIL RUNS
* REUTERS128 - http://gerbil.aksw.org/gerbil/experiment?id=201611210001
* KORE50 - http://gerbil.aksw.org/gerbil/experiment?id=201612110002

#### Later
* Include NIL Clustering
