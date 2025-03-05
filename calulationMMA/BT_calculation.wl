(* ::Package:: *)

(* \:5df2\:77e5\:53c2\:6570 *)
b = 4.318;       (* \:77e9\:5f62\:6ce2\:5bfc\:77ed\:8fb9 mm *)
lambdaGr = 21.86; (* \:77e9\:5f62\:6ce2\:5bfc\:5de5\:4f5c\:6ce2\:957f mm *)
dia = 2*5.754;   (* \:5706\:6ce2\:5bfc\:76f4\:5f84 mm\:ff0c\:6839\:636e\:6587\:6863\:4e2dR=5.754mm\:8ba1\:7b97 *)

(* \:4e2d\:95f4\:53c2\:6570\:8ba1\:7b97 *)
beta = 2 Pi/lambdaGr;
phi = (Pi b)/dia;

(* \[Delta]\:51fd\:6570\:5b9a\:4e49 *)
Delta2n[n_] := 1/Sqrt[1 - (beta dia/(2 Pi n))^2] - 1

(* \:6c42\:548c\:9879\:8ba1\:7b97\:ff08\:524d5\:9879\:ff09 *)
sumTerm = 2 Sum[(Sin[n phi]^2)/(n^3 phi^2) * Delta2n[2n], {n, 1, 5}];

(* \:5b8c\:6574B\:209c\:8ba1\:7b97 *)
BT = b/lambdaGr * (
   2 Log[(dia^2 - b^2)/(4 b dia)] 
   + (b/dia + dia/b) Log[(dia + b)/(dia - b)]
   + sumTerm
);

(* \:7ed3\:679c\:8f93\:51fa *)
Print["\:7b49\:6548\:7535\:7eb3 B_T = ", BT]
