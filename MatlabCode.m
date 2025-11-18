
% Written program of run test in Matlab
%
%Input: time series data- a=[];
%
mean(a);

zz=a-mean(a);

n=0;
m=0;
for i=1:N-1
    
    if zz(i)>0 & zz(i+1)>0 
        n=n+1;
    end 
    if zz(i)<0 & zz(i+1)<0
        m=m+1;
    end
end 
%
%Output: total number of runs=m+n 
