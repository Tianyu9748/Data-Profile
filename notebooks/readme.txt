Nutrition label:

First , we used pandas_profiling module to generate basic information about the dataset, like. distribution of each features, interaction between each features. sample dataset etc.

Next thing is to find any bias that may exist in the datset, we do that by finding funtional dependencies of the each features. 
Cell-9:
we take the dataset .csv file and pass it through our main function inside the fdtool script along with the sample size(since it takes time to generate , we are sampling from the dataset, we are not passing the whole dataset).
we get two list FD, ASSC.
Cell-10:
we are filtering through the FD list to find all the subsets that are uniquely determines our protected attributes. Then we are passing the list to plot the graph.
Cell-12-13:
we are doing the same thing we the ASSC list filtering and passing the data to the Network.


fdtool.py:
line-83:
we are rading the csv file using pandas library and takinga sample of the dataset based sample num that we passed.
line-103:
we create a list (U) and store the header names of our dataset,(Feature names). and we initilize a counter variable k=0 for later use.
line-106:
we create a dictionary(Alpha_Dict) , and convert our list (U) into a alphabetical order.
line-113:
we take the length(L) of our list(U)
we are initilizing lattice with singleton set at level-1. which means we create list(C) of same size(L). and appending the array with the value of None for another L length.
line-115:
we create a Subset generate(SG).
we create poweset(PO) we pass our header name list (U) in to the powerset function in the Apriori_Gen script
Here we generate next k-level attributes subset by appending a list with x where is in the PO if length of x is equal to the k, where k is in the range of (length of PO)+1
line-118:
Here we are creating a dictionary(Closure), which is a dicitonary of binary representation of every attributes available. for every subset(sg) we get from our subset generater(SG). we pass that into the toBin function in binaryRepr script to get bianry representation of that subset(br), and append the Closure dicitonary with {subset: binary representaion(br)}
line-120:
Now  we create a dictionary called (Cardinality) , and basically append None each element of the dictionary(Closure). this dictionary is same as Closure with just None value of each value, instade of attribute names.
line-122-125:
Here we are just initilizing a list called (Counter) with value [0,0] for later. and we also initilize two empty list called FD and E_set. We also initilize FD_return to store our Functional dependencies subsets and ASCC to store association rules subsets later on.
line-126:
we are initilizing a while loop with argument 'True'.Meaning loop does not stop unless we itentionally break it.
line-129:
we increment the counter variable(k) that we created in line-103. we also create a vriable(c_km1) and assign it the (k-1)th element of the list (C) that we created in line-103.
line-131-133:
we update the dictionary (Closure) and also update the dictionary(Cardinality) to next k-level subset. Basically we repeat the same process as we did in line-118 and line-120 with an increament of k.
line-135-139:
here we find the dereference of closure and Cardinality at k-2 level. if k greater than 1, for each subset at (k-1)th element of the list(C). we pass the subset and the list U into the toBin function of bianryRepr.py script to get the binary representation(br). then we delete the (br)th element of the Dictionary(Closure) and (br)th element of (Cardinality).
Then we assign None value into the (k-2)th element of thr list C.
line-143:
we pass c_km1 variable that we created in line-129 into the oneUp function in the Apriori_Gen.py script to find k-level attribute row from (k-1) lavel attribute row.
we get variable(C_k) which is binary represtatin of every attribute appended with every (k-1) level subset.
line-145:
here we are getting the list of subsets(F)( which is Funstional Dependencies we want), upaded Closure dictionary, and updated Cardinality dictionary by passing variables (C_km1), the dataset we get (df), Closure dictionary we have right now ,the Header list(U) and the Cardinality variable we have rigth now.
line-147:
In this line we try to find the association rules subsets by calculating the Equivalences(E) by passing the (C_km1), (F), Closure dictionary that we get from above and the header list(U).
line-149:
In this line we are initilizing (C_k) (a list of reduced subset from E).
We are reducing the K-level iteration and remove/modify the E, by passing the varibles E,C_k, Closure, and the dataset to a function (f) in Prune.py script.
It returns updated Closure dictinary, C_k list, and the dataset.
line-151:
In this line we are updating the (Counter) variable. with values - length of eqivalences(E) and length of (F).
we are also appendinf the list (E_set) with the value E.
line-153-159:
for each item(f) in the list (F) we are appending our (FD_return) list with the value of (f). we check if current (C_k) greater than zero , if not we break the Infinite while loop that we created.

for every item(e) in list(E_set), we are appending the (ASCC) list with the value of e.
then we are returning the those two list (FD-return) and (ASCC)


Prune.py:
line-29: this function take list of subsets(C_k), Eqivalence(E), Closure Dicitonary, dataset(df), and header list(U). returns the list of subsets not to be removed, updated Closure Dictionary, dataset.
line-32: 
we define empty list(SetsToRemove).
line-35-71:
for each sets(S) in list(C_k), we get.
we pass C_k into the oneDown function in Apriori_gen.py script to get k-1 level subsets(M1)

for each set(x) in list(M1) we are getting value (M2) from closure decitionary from the key of [binaryrepr.toBin(x, U)]. then we are checking if length of M2 is greater than 1, and x is a subset of sets(S). we are putting exclusive closure of x in union with inclusive closure of S; S^{+} = S^{+} U X^{*}.
In order to check whether any of x is consequent of any of Equivalence(E).
for set(EQ) in E, we are checking if any of set(x) is equal to set(EQ). then we are checking if set(S) is contained in Closure value at binaryRepr.toBin(x, U) key point. if so we are appending the (SetsToRemove) with value of S.
line-74:
for each item ck in C_k , if ck is not present in (SetsToRemove) list we are return that value as an updated C_K list.

----------------------------------------------------------------------------------------------------------

ObtainEquivalences.py:
line-13:
this function takes C_km1, Functional dependence(F), Closure dicitonary, and the Header list(U)
line-16:
we are initilizing the Empty list E.
line-19-27:
for each item(X) in C_km1, and for each item(Y) in in F, we try finding two sets
1. we are passing X and U into the toBin function to get key K and getting set A value from the Closure dicitonary at K key point.
2. we are passing 0th index of Y and U to toBin function to get K1 and getting the set A1 value from the Closure dictionary at K1 key point.

Then we are checking if set X in subset of K1 and Y[0] is the subset of K. if those holds true we are appending the list E with value X and 0th element of Y.

----------------------------------------------------------------------------------------------------------
GetFDs.py: This function takes the variable(C_km1), the dataset, the binary representation of subset dictionary(Closure), the header name list(U), and the Dictionary(Cardinality) , Returns the Functinal Dependency list, updated (Cradinality) and updaed (Closure)
line-45:
We are initilizing empty list F. and getting the remaining attributes name U_c
line-48:
Here we are creating (SubsetsToCheck) variable , appending it with subset for every subset in set(candidate+v_i) for each candidate in C_km1 and for every v_i in a list where (Diff_Set). 
where Diff_Set is diffrence between the set(U_c) and the set of Closure[Binary_Repr(candidate, v_i)]
line-54:
for every item(Cand) of (SubsetsToCheck) ,every item(Card) in (CardofPartition). 
we find Binary Representation(BiCand) of (Cand, U) by paasing those to the toBin function of BinaryRepr.py script. and we append Cardinality ditionary by assigning the Card variable to the (BiCand)th key of the Cardinality.
line-59-67:
fro each (candidate) in the list C_km1. we find list(V_I), which is diffrence between set(U_c) and the set we get by passing (candidate), the list (U) to Closure dictionary.
for each item(v_i) in the list(V_I), we find two sets 
1. we get by passing (candidate) and (U) to toBin function. and pass this to the Cardinality Dictionary .
2. this we get by poassing (candidate+v_i) and (U) to toBin function, and pass this to the Cardinality Dictionary.

if above two sets are equal the we update the key[toBin(candidate, U)] of Closure dicitonary with the value of v_i
and we append the Functional_Dipendency list with the value (candidate, v_i).
line-69:
we return Closure dictionary, F list, Cardinality dictionary.



----------------------------------------------------------------------------------------------------------
Apriori_Gen.py:
line-7: This function takes a list(s) and returns powersets of that list.
line-8:
we take length of the given list(x). then we create a empty list named(powerset).
line-11:
we calculate range( 1 << x).Which is 1 with bits shifted to the left by x places.It is same as multiplying 1 by 2**x. we take this range, for each i in range we append list(powerset) that we created, with the value of s[j], where j is in the range of length(x) if i and (1 << j) is same.
line-13:
then we return the list(powerset)

line-15: This functions take a list of attributes and returns a list of subsets with one level up from groud list. etc. input--> [A, B, C] return -->[[C,B],[B,A]]
line-17:
we flatten the list given(C_km1),if the list has more than one dimension, in our case it is.
line-20-23:
Then we pass the flatten list that we created and pass it through the powerset function in line-7, to get subset generater of the list.
we return list of subsets we created above if length of subset is equal to length of next item of the list(C_km1)+1


----------------------------------------------------------------------------------------------------------
binaryRepr.py
line-3: This functions takes attribute(C) and a list(U) containing all attributes and returns a dictionary of binary representation of the attributes.
line-4:
we craete a list(Gen) . we are appending them with 1 if k is in present in the list(U) , otherwise 0 , for k in range of length of (U)
then we are joining the list with blank string operater to convert that into a string.
line-8:
then we return the joined string that we created.
