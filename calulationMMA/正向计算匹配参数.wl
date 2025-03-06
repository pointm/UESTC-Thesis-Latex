(* ::Package:: *)

CreateWindow@PaletteNotebook@Dynamic[Grid[
    Select[
     With[{expr = ToExpression@#},
        {#,
         Head[expr],
         Which[
          ListQ[expr], Dimensions[expr],
          NumericQ[expr], expr,
          StringQ[expr], StringLength[expr],
          True, "-"]}] & /@ Names["Global`*"],
     (#[[2]] =!= Symbol) &],
    Alignment -> Left],
    UpdateInterval -> 10, TrackedSymbols->{}]



(* \:53c2\:6570\:5b9a\:4e49 *)
a = 10.668*^-3; (* \:77e9\:5f62\:6ce2\:5bfc\:957f\:8fb9\:ff0c\:5355\:4f4dm *)
b = 4.3188*^-3;  (* \:77e9\:5f62\:6ce2\:5bfc\:77ed\:8fb9\:ff0c\:5355\:4f4dm *)
f = 19.65*^9;  (* \:5339\:914d\:9891\:70b9\:ff0c\:5355\:4f4dHz *)
omega=2 Pi f; (*\:5339\:914d\:9891\:70b9\:89d2\:9891\:7387\:ff0c\:5355\:4f4dHz*)
c=3*10^8; (* \:5149\:901f\:ff0c\:5355\:4f4dm/s *)
\[CurlyEpsilon]r = 9.4;   (* \:84dd\:5b9d\:77f3\:76f8\:5bf9\:4ecb\:7535\:5e38\:6570 *)
\[Mu]11 = 1.841; (* \:5706\:6ce2\:5bfcTE11\:6a21\:7279\:5f81\:503c\:ff0c\:672c\:6765\:8981\:5e26\:4e00\:6487\:7684 *)

(* \:5706\:6ce2\:5bfc\:534a\:5f84\:8ba1\:7b97 *)
Dia = Sqrt[a^2 + b^2]; (* \:77e9\:5f62\:6ce2\:5bfc\:5bf9\:89d2\:7ebf\:4f5c\:4e3a\:5706\:6ce2\:5bfc\:76f4\:5f84 *)
R = Dia/2; (* \:5706\:6ce2\:5bfc\:534a\:5f84 *)

(* \:81ea\:7531\:7a7a\:95f4\:6ce2\:957f\:8ba1\:7b97 *)
lambda = c/(f); (* \:6ce2\:957f\[Lambda] = c/f\:ff0c\:5355\:4f4dmm *)


(* \:77e9\:5f62\:6ce2\:5bfc\:622a\:6b62\:6ce2\:957f\:4e0e\:5de5\:4f5c\:6ce2\:957f\:8ba1\:7b97 *)
lambdaCRect = 2a; (* \:77e9\:5f62\:6ce2\:5bfc\:622a\:6b62\:6ce2\:957f *)
lambdaGRect = lambda / Sqrt[1 - (lambda/lambdaCRect)^2]; (* \:5de5\:4f5c\:6ce2\:957f *)

(* \:5706\:6ce2\:5bfc\:622a\:6b62\:6ce2\:957f\:4e0e\:5de5\:4f5c\:6ce2\:957f\:8ba1\:7b97 *)
lambdaCCirc = (2 \[Pi] R)/\[Mu]11; (* \:5706\:6ce2\:5bfc\:622a\:6b62\:6ce2\:957f *)
lambdaGCirc = lambda / Sqrt[1 - (lambda/lambdaCCirc)^2]; (* \:5de5\:4f5c\:6ce2\:957f *)

Print["\:77e9\:5f62\:6ce2\:5bfc\:7684\:622a\:6b62\:6ce2\:957f\:662f\:ff1a" ToString[lambdaCRect*1000]"mm"]
Print["\:5de5\:4f5c\:6ce2\:957f\:662f"ToString[lambdaGRect*1000]"mm"]
Print["\:5706\:67f1\:5f62\:6ce2\:5bfc\:7684\:622a\:6b62\:6ce2\:957f\:662f\:ff1a" ToString[lambdaCCirc*1000]"mm"]
Print["\:5de5\:4f5c\:6ce2\:957f\:662f"ToString[lambdaGCirc*1000]"mm"]

(*\:8ba1\:7b97\:77e9\:5f62\:4e0e\:5706\:6ce2\:5bfc\:4e4b\:95f4\:7684\:7535\:7eb3BT*)

(* \:4e2d\:95f4\:53c2\:6570\:8ba1\:7b97 *)
beta = 2 Pi/lambdaGRect;
phi = (Pi b)/Dia;

(* \[Delta]\:51fd\:6570\:5b9a\:4e49 *)
Delta2n[n_] := 1/Sqrt[1 - (beta Dia/(2 Pi n))^2] - 1

(* \:6c42\:548c\:9879\:8ba1\:7b97\:ff08\:524d5\:9879\:ff09 *)
sumTerm = 2 Sum[(Sin[n phi]^2)/(n^3 phi^2) * Delta2n[2n], {n, 1, 5}];

(* \:5b8c\:6574BT\:8ba1\:7b97 *)
BT = b/lambdaGRect * (
   2 Log[(Dia^2 - b^2)/(4 b Dia)] 
   + (b/Dia + Dia/b) Log[(Dia + b)/(Dia - b)]
   + sumTerm
);

(* \:7ed3\:679c\:8f93\:51fa *)
Print["\:7b49\:6548\:7535\:7eb3 B_T = ", BT]


(*\:8ba1\:7b97\:77e9\:5f62\:6ce2\:5bfc\:4e0e\:5706\:6ce2\:5bfc\:7684P-V\:5b9a\:4e49\:7684\:7279\:5f81\:963b\:6297\:4e4b\:6bd4 k*)
ZRect=2*b/a*120*Pi/Sqrt[1-(c/(2*a*f))^2];
ZCirc=2.02*120*Pi/Sqrt[1-(c/(3.413*R*f))^2];
k=ZCirc/ZRect;  (*\:6ce8\:610f\:5f52\:4e00\:5316\:5bf9\:8c61*)
Print["\:5f52\:4e00\:5316\:5706\:6ce2\:5bfc\:7279\:6027\:963b\:6297 = ", k]

(*\:4e3a\:4e86\:786e\:4fdddelta\:5927\:4e8e\:96f6\:ff0c\:8ba1\:7b97Bd\:7684\:6700\:5927\:503c\:ff0c\:6b64\:65f6\:53ef\:4ee5\:8ba1\:7b97\:5f97\:5230\:7a97\:7247\:7684\:539a\:5ea6\:54e6~*)
Bdmin=0;
Bdmax=Sqrt[(1+BT^2)^2*k^4+2 (BT^2-1) k^2 + 1]/k;
Print["Bd\:7684\:6700\:5927\:503c = ", Bdmax]

tmax=Bdmax/((\[CurlyEpsilon]r-1)(omega/c)(lambdaGCirc/lambda));
Print["\:7a97\:7247\:539a\:5ea6\:7684\:6700\:5927\:503c = ", tmax*1000]

(*\:8fdb\:884c\:4e8c\:6b21\:65b9\:7a0b\:7684\:6c42\:89e3*)
BdRange = {0.01, Bdmax};  (* \:6765\:81eadelta\:7684Bd\:7ea6\:675f\:ff0c\:9632\:6b62Bd\:4e3a0 *)


gammaRect=2 Pi /lambdaGCirc;  (* \:539f\:4ee3\:7801\:4e2dlambdaGC\:5e94\:8be5\:662flambdaGCirc *)

(* \:4fee\:6539\:51fd\:6570\:540d\:907f\:514d\:51b2\:7a81 *)
Acoeff[Bd_] := k*(Bd*(BT^2 + 1)*k - 2*BT);
Bcoeff[Bd_] := 2 - 2*k*(BT*(Bd + BT*k) + k);
Ccoeff[Bd_] := Bd + 2*BT*k;


(* \:53ef\:89c6\:5316\:89e3\:7684\:539f\:59cb\:6570\:636e\:7ed3\:6784 *)
BdValues = Subdivide[First@BdRange, Last@BdRange, 50]
realSolutions = Table[
   {BdVal, #} & /@ solveTanGammaL[BdVal],
   {BdVal, BdValues}];

(* \:65b0\:589e\:ff1a\:5c06\:89e3\:5bfc\:51fa\:4e3a\:4e24\:4e2a\:5206\:79bb\:7684\:6570\:7ec4 *)
bdList = First /@ Flatten[realSolutions, 1];      (* \:6240\:6709Bd\:503c\:7684\:4e00\:7ef4\:6570\:7ec4 *)
tanGammaList = Last /@ Flatten[realSolutions, 1]; (* \:6240\:6709tan(\[Gamma]l)\:7684\:4e00\:7ef4\:6570\:7ec4 *)

(* \:6216\:8005\:5bfc\:51fa\:4e3a{ {Bd, tan\[Gamma]l}, ... } \:683c\:5f0f\:7684\:89e3\:5bf9 *)
solutionPairs = Flatten[realSolutions, 1];        (* \:4fdd\:6301Bd\:4e0e\:89e3\:7684\:5bf9\:5e94\:5173\:7cfb *)

ListPlot[Flatten[realSolutions, 1], 
 PlotStyle -> Red,
 AxesLabel -> {"Bd", "tan(\[Gamma]l)"}, 
 PlotLabel -> "\:5b9e\:6570\:89e3\:5206\:5e03"]




Print[realSolutions]
