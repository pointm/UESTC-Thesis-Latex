(* ::Package:: *)

(* \:5b9a\:4e49\:5df2\:77e5\:53c2\:6570 *)
k = 2.77099;
Bt = 0.262507;
BdRange = {0, 2.65351};  (* \:6765\:81ea\:6587\:6863\:7684Bd\:7ea6\:675f *)

(* \:5b9a\:4e49\:4e8c\:6b21\:65b9\:7a0b\:7cfb\:6570 *)
A[Bd_] := k*(Bd*(Bt^2 + 1)*k - 2*Bt);
B[Bd_] := 2 - 2*k*(Bt*(Bd + Bt*k) + k);
Cc[Bd_] := Bd + 2*Bt*k;  (* \:907f\:514d\:4e0e\:4fdd\:62a4\:7b26\:53f7C\:51b2\:7a81 *)

(* \:6c42\:89e3\:8d85\:8d8a\:65b9\:7a0b\:7684\:51fd\:6570 *)
solveTanGammaL[BdVal_] := Module[{a, b, c, solutions},
  a = A[BdVal];
  b = B[BdVal];
  c = Cc[BdVal];
  
  solutions = NSolve[a*t^2 + b*t + c == 0, t];
  
  (* \:8fc7\:6ee4\:5b9e\:6570\:89e3\:5e76\:8f6c\:6362\:4e3a\:89d2\:5ea6\:89e3 *)
  Select[t /. solutions, Element[#, Reals] &]
]

(* \:793a\:4f8b\:8ba1\:7b97\:ff1a\:53d6Bd=0.5\:65f6 *)
exampleSolutions = solveTanGammaL[2.65];
Print["\:5f53Bd=2.65\:65f6\:ff0ctan(\[Gamma]l)\:7684\:5b9e\:6570\:89e3\:4e3a\:ff1a", exampleSolutions]

(* \:53ef\:89c6\:5316\:89e3\:7684\:5206\:5e03 *)
BdValues = Subdivide[First@BdRange, Last@BdRange, 50];
realSolutions = Table[
   {BdVal, #} & /@ solveTanGammaL[BdVal],
   {BdVal, BdValues}];
 
ListPlot[Flatten[realSolutions, 1], 
 PlotStyle -> Red,
 AxesLabel -> {"Bd", "tan(\[Gamma]l)"}, 
 PlotLabel -> "\:5b9e\:6570\:89e3\:5206\:5e03"]


bdNow=2.547;
tanGama=0.36;
lambdaGC=24.27/1000;
f=19.65*10^9;
c=3*10^8;

lambda=c/f;
thickWindow=1000*bdNow*c*lambda/(8.4*2*Pi*lambdaGC*f)
gama=2*Pi/(lambdaGC);

length=1000*ArcTan[tanGama]/gama




