function [X, ndx, dbg] = natsortfiles(X, rgx, varargin)

%% Input Wrangling

assert(iscell(X),...
	'SC:natsortfiles:X:NotCellArray',...
	'First input <X> must be a cell array.')
tmp = cellfun('isclass',X,'char') & cellfun('size',X,1)<2 & cellfun('ndims',X)<3;
assert(all(tmp(:)),...
	'SC:natsortfiles:X:ContentNotCharVectors',...
	'First input <X> must be a cell array of strings (1xN character).')

ide = cellfun(@(s)ischar(s)&&strcmpi(s,'noext'),varargin);
assert(nnz(ide)<2,...
	'SC:natsortfiles:options:noextOverspecified',...
	'File-extension handling is overspecified.')
varargin(ide) = [];

if nargin>1
	varargin = [{rgx},varargin];
end

%% Split and Sort File Names/Paths

% Split full filepaths into file [path,name,extension]:
[pth,fnm,ext] = cellfun(@fileparts,X(:),'UniformOutput',false);

% Split path into {dir,subdir,subsubdir,...}:
pth = regexp(pth,'[^/\\]+','match'); % either / or \ as filesep.
len = cellfun('length',pth);
num = max(len);
vec = cell(numel(len),1);

if any(ide)
	fnm = strcat(fnm,ext);
	ext(:) = {''};
end

% Alphanumeric sort of the file extensions and filenames:
if isempty(num)
	ndx = [];
	ids = [];
	dbg = {};
elseif nargout<3 
	[~,ndx] = natsort(ext,varargin{:});
	[~,ids] = natsort(fnm(ndx),varargin{:});
else
	[~,ndx,dbg{num+2}] = natsort(ext,varargin{:});
	[~,ids,tmp] = natsort(fnm(ndx),varargin{:});
	[~,idd] = sort(ndx);
	dbg{num+1} = tmp(idd,:);
end
ndx = ndx(ids);

% Alphanumeric sort of the directory names:
for k = num:-1:1
	idx = len>=k;
	vec(:) = {''};
	vec(idx) = cellfun(@(c)c(k),pth(idx));
	if nargout<3 
		[~,ids] = natsort(vec(ndx),varargin{:});
    else
		[~,ids,tmp] = natsort(vec(ndx),varargin{:});
		[~,idd] = sort(ndx);
		dbg{k} = tmp(idd,:);
	end
	ndx = ndx(ids);
end

% Return the sorted array and indices:
ndx = reshape(ndx,size(X));
X = X(ndx);

end