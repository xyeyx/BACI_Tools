* Not Recommended! It is 6 times slower than Python...

* Utility of slicing BACI into smaller files per HS4 instead of per year.
* -------------------------
* A: Xianja Ye
* E: X[d0t]Ye[8]rug.nl
* Groningen Growth & Development Centre
* University of Groningen
* -------------------------

timer on 1
mata:


function create_file(string HS4) {
    filename = "HS4_"+ HS4 + ".csv";
    f = fopen(filename, "w");
    fput(f, "y,i,j,k,v,q");
    fclose(f);
}



function write_to_file(HS4, pointer(transmorphic) DATA_STOR, scalar l) {
    DATAOUT = asarray(*DATA_STOR, HS4);
    filename = "HS4_"+ HS4 + ".csv";
    tmpstr="";
    for (i = 1; i<=l; i++) {
        tmpstr = tmpstr + subinstr(DATAOUT[i]," ","") + char(13);
    }
    f = fopen(filename, "a");
	fwrite(f, tmpstr);
	fclose(f);
}

function HS_extract(string line, scalar level) {
    tmpstr = substr(line, ustrpos(line, ",")+1,);
	tmpstr = substr(tmpstr, ustrpos(tmpstr, ",")+1,);
	tmpstr = substr(tmpstr, ustrpos(tmpstr, ",")+1,);
	return(substr(tmpstr, 1, level));
}

function line_appending(string line,  pointer(transmorphic) HS_COUNTER, pointer(transmorphic) DATA_STOR) {
    HS4 = HS_extract(line, 4);
    if (asarray_contains(*HS_COUNTER, HS4)) {
        count = asarray(*HS_COUNTER, HS4);
        if (count>0) {
            new_count = count + 1;
            asarray(*HS_COUNTER, HS4, new_count);
            (asarray(*DATA_STOR, HS4))[new_count]=line;
            
            if (new_count > 2999) {
                write_to_file(HS4, DATA_STOR, 3000);
                asarray(*HS_COUNTER, HS4, 0);
                asarray_remove(*DATA_STOR, HS4);
            }
            ;            
            
        }
        else {
            asarray(*HS_COUNTER, HS4, 1);
            asarray(*DATA_STOR, HS4, J(3000,1,""));
		    (asarray(*DATA_STOR, HS4))[1]=line;
        }
    }
    else {
        create_file(HS4);
        asarray(*HS_COUNTER, HS4, 1);
        asarray(*DATA_STOR, HS4, J(3000,1,""));
		(asarray(*DATA_STOR, HS4))[1]=line;
    }
}


function cache_allwrite(pointer(transmorphic) HS_COUNTER, pointer(transmorphic) DATA_STOR){
    HS_ALL = asarray_keys(*HS_COUNTER);
    Num_HS  = length(HS_ALL);
    for (i = 1; i<= Num_HS; i++) {
        HS4 = HS_ALL[i];
        if ((l=asarray(*HS_COUNTER, HS4)) > 0) {
            write_to_file(HS4, DATA_STOR, l);
            asarray(*HS_COUNTER, HS4, 0);
            asarray(*DATA_STOR, HS4, NULL);	           
        }
        ;
    }
}



DATA_STOR = asarray_create("string", 1)
HS_COUNTER = asarray_create("string", 1)


filename = "RAW_DATA/BACI_HS07_Y2007_V202401.csv"

f = fopen(filename, "r");
line = fget(f);

while ((line=fget(f))!=J(0,0,"")) {
     // line = ustrtrim(line);
    if (strlen(line)<6) {
        continue;
    }
    else {
        line_appending(line, &HS_COUNTER, &DATA_STOR);
    }
}

cache_allwrite(&HS_COUNTER, &DATA_STOR);


fclose(f)

end
timer off 1
timer list 1
