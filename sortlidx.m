function [B, I] = sortlidx(A, dim, varargin)

if nargin == 1
    dim = find(size(A)>1,1); 
    if isempty(dim), dim = 1; end
end

if nargout == 1
    B = sort(A,dim,varargin{:});
    return
end

sz = size(A);
N = numel(sz);

if dim > N
    B = A;
    I = reshape(1:numel(A),sz);
    return
end

gv = arrayfun(@(a)1:a,sz,'uni',0);
[F{1:N}] = ndgrid(gv{:});
[B,F{dim}] = sort(A,dim,varargin{:});
I = sub2ind(sz,F{:});