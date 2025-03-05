(* ::Package:: *)

(* \:4ee3\:6570\:6c42\:89e3\:8fc7\:7a0b *)
\[CapitalDelta] = 4 - 4*(2 + Bd^2 - 2*Bt^2)*k^2 + 4*(1 + Bt^2)^2*k^4;
solution = Reduce[\[CapitalDelta] > 0 && k > 0 && Bt > 0, Bd];

(* \:4ee3\:5165\:6587\:6863\:4e2d\:7684\:6570\:503c *)
k = 2.77099;
Bt = 0.262507;
BdRange = solution /. {k -> 2.77099, Bt -> 0.262507} // N;

Print["\:89e3\:6790\:89e3\:8868\:8fbe\:5f0f\:ff1a", solution]
Print["\:6570\:503c\:89e3\:7ed3\:679c\:ff1a", BdRange]


Bt=0.262507
k=2.77099
x=Sqrt[(1+Bt^2)^2*k^4+2(Bt^2-1)k^2+1]/k


f=19.65*^9; 
omega = 2*Pi*f;
c=3*^8;
a=10.668/1000
b=4.318/1000
R=Sqrt[a^2+b^2]/2
lambda=c/f;
niu11=1.841;
lambdaC=2*Pi*R/niu11;
alpha=2.653513991148635;

windowThick=alpha*Sqrt[1-(lambda/lambdaC)^2]/((9.4-1)*(omega/c));
Print["\:539a\:5ea6\:662f" ToString[windowThick*1000]]



