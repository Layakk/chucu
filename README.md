# CHUCU

This sofware is a modified version of the UPX packer that allows a user to obfuscate other software to try to avoid detection by Antivirus.

## DISCLAIMER

This site contains materials that can be potentially damaging or dangerous. If you do not fully understand something on this site, then GO OUT OF HERE! Refer to the laws in your province/country before accessing, using, or in any other way utilizing these materials. These materials are for educational and research purposes only. Do not attempt to violate the law with anything contained here. If this is your intention, then LEAVE NOW! Neither administration of this server, the authors of this material, or anyone else affiliated in any way, is going to accept responsibility for your actions. DON'T USE THIS SOFTWARE except for research purposes.

Please read the LICENSE for more information.

## NOTE

This program is not a finished program, but a work in progress. It's probably full of bugs and things that need improvement. Please, be patient and use it with care.

All ideas and contributions are welcome.

## Prerequisites

Before you can run this program on your PC you'll need:
  * [UPX tools v20130920](https://github.com/upx/upx-stubtools/releases/tag/v20130920). Install it and add the installation folder to $PATH.
  * [VirusTotal API Key](https://developers.virustotal.com/reference#getting-started)
  
## Running

### Running lk_generate_specimen.sh

This executable is used to create a new specimen with some parameters specified in the command line:

| Parameter | Format | Description |
| :-------: |:------:| :----- |
| -i | filename's abs. path | Input file. |
| -o | filename's abs. path | Output file. |
| -f | - | Deletes output file if exists withot asking. |
| -m | <min>,<max> | Minimum and maximum block instruction size. |
| -c | - | Activates code ciphering. |
| -r | - | Activates resources ciphering. |
| -s | number | Lower bound for resources ciphering. |
| -p | number | Higher bound for resources ciphering. |
| -t | number | Add plain text and establish the number of Bytes added. |
| -b | filename's abs. path | Indicates source for plain text. |


Example:

```
./lk_generate_specimen.sh -i /path/to/my/program.exe -o /path/to/my/out_program.exe -f -m 5,10 -c -r -s 100 -p 4000 -t 5000000 -b /path/to/different/plain_text_source.txt 
```

### Running lk_find_valid_specimen.py

This executable is used to find the best parametrization to obfuscate an executable.
You must edit the parametrization before running this program:

| Parameter | Format | Description |
| :-------: |:------:| :----- |
| APIKEY | String APIKEY | Virustotal API Key String |
| in_specimen_real | filename's abs. path | Input executable file. |
| OUTPUTDIR | Folder's abs. path | Output directory for generated executables. |
| CSVFILE | filename's abs. path | Output CSV with results. |
| RS_ARR | Integer array | List of lower bounds for resources ciphering to be tested. |
| RS_ARR_TOP | Integer array | List of highers bound for resources ciphering to be tested. |
| TM_ARR | Integer array | List of bytes added as plain text to be tested. |
| JMPS | String array | List of paris of minimum and maximum block instruction to be tested. |
  

```
APIKEY='####### API KEY #######'
in_specimen_real='/path/to/my/program.exe'

OUTPUTDIR='/path/to/my/out_program.exe'
EXTENSION='.exe'

CSVFILE='/path/to/my/specimens.csv'

RS_ARR=[10, 100, 1000, 2000]
RS_ARR_TOP=[0, 10, 100, 1000]
TM_ARR=[1000, 3000, 7000, 10000, 20000, 30000]
JMPS=["3,5","5,7","5,10"]
```

Example:


```
./lk_find_valid_specimen.py
```


## Authors

Layakk Seguridad Informatica S.L.

## License

This project is licensed under the GPL license - see the [LICENSE](LICENSE) file for details
