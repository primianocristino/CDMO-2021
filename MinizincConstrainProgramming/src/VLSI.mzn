include "globals.mzn";

int: w; % width of the plate
int: n; % #circuits
array[1..n] of int: W; % width of circuits
array[1..n] of int: H; % Height of circuits

int: minArea = sum(i in 1..n)(W[i]*H[i]);
int: maxAreaW = sum(i in 1..n)(H[i]*max(W));
int: maxAreaH = sum(i in 1..n)(max(H)*W[i]); 
int: downH = minArea div w;
int: upH = min(maxAreaH,maxAreaW) div w;

array[1..n] of var int: x; % x of circuits
array[1..n] of var int: y; % y of circuits
var downH..upH: h; % lenght of the plate

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Predicates%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

predicate no_overlap_2d(array[int] of var int: x, array[int] of var int: y,array[int] of var int: W, array[int] of var int: H) =
forall(i,j in 1..n where i!=j)(
  ((x[j]>=x[i] /\ x[j]<x[i]+W[i]) -> (y[i]+H[i]<=y[j] \/ y[j]+H[j]<=y[i])) /\
  ((y[j]>=y[i] /\ y[j]<y[i]+H[i]) -> (x[i]+W[i]<=x[j] \/ x[j]+W[j]<=x[i])) /\
  
  ((x[i]>=x[j] /\ x[i]<x[j]+W[j]) -> (y[i]+H[i]<=y[j] \/ y[j]+H[j]<=y[i])) /\
  ((y[i]>=y[j] /\ y[i]<y[j]+H[j]) -> (x[i]+W[i]<=x[j] \/ x[j]+W[j]<=x[i]))

);

predicate orderSameShape(array[int] of var int: W, array[int] of var int: H)=  
forall(i,j in 1..n where i<j)(
      ((W[i]==W[j] /\ H[i]==H[j]) -> (x[i]+W[i]<= x[j] \/ y[i]+H[i] <= y[j] )) 
  );
  

predicate orderRectMaxLength(array[int] of var int: coord,var int: lato,array[int] of var int: arrayLato, array[int] of var int: arrayLatoOpposto)=   
forall (i,j in 1..n where arrayLato[i]==lato /\  i<j)(
      (coord[i]+arrayLatoOpposto[i]<=coord[j])
); 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Main model constraints%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

constraint forall(i in 1..n)(x[i]>=0 /\ y[i]>=0 /\ x[i]+W[i]<=w /\ y[i]+H[i]<=h);
constraint no_overlap_2d(x,y,W,H);
constraint forall(offset_x in 1..w)(
  sum(rect in 1..n where x[rect]<=offset_x /\ offset_x<x[rect]+W[rect])(H[rect])<=h
);


%%%%%%%%%%%%%%%%%%%%%%%%%%Symmetry breaking constraints%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

constraint orderRectMaxLength(y,w,W,H);
constraint orderRectMaxLength(x,h,H,W);
constraint orderSameShape(W,H);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Objective Function%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% variable selections:
ann : varChoise
%         = input_order
%         = first_fail
%         = anti_first_fail
%         = smallest
%         = largest
%         = occurence
%         = most_constrained
%         = mex_regret
        = dom_w_deg
;

% value selections:
ann : valChoise
%          = indomain_min
%          = indomain_max
%          = indomain_middle
%          = indomain
%          = indomain_interval
%          = indomain_median
%          = indomain_random
%          = indomain_split
          = indomain_reverse_split
;

solve  ::seq_search([
  int_search([h], input_order, indomain_min,complete),
  int_search(x,varChoise,valChoise,complete),
  int_search(y,varChoise,valChoise,complete),
])
 minimize h;
 
output 
["height = ",show(h), "\n"] ++
["width = ",show(w), "\n"] ++
["\n"]++
["x = ", show(x), "\n"] ++
["y = ", show(y), "\n"]++
["\n"]++
["W = ", show(W), "\n"]++
["H = ", show(H), "\n"];
