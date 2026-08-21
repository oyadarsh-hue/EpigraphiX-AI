function varargout = run_gui(varargin)
% RUN_GUI MATLAB code for run_gui.fig
%      RUN_GUI, by itself, creates a new RUN_GUI or raises the existing
%      singleton*.
%
%      H = RUN_GUI returns the handle to a new RUN_GUI or the handle to
%      the existing singleton*.
%
%      RUN_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in RUN_GUI.M with the given input arguments.
%
%      RUN_GUI('Property','Value',...) creates a new RUN_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before run_gui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to run_gui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help run_gui

% Last Modified by GUIDE v2.5 14-Sep-2025 17:57:38

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @run_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @run_gui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before run_gui is made visible.
function run_gui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to run_gui (see VARARGIN)

% Choose default command line output for run_gui
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes run_gui wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = run_gui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

set(handles.pushbutton2, 'Enable', 'off');
set(handles.pushbutton3, 'Enable', 'off');
set(handles.pushbutton4, 'Enable', 'off');
set(handles.pushbutton5, 'Enable', 'off');


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

set(run_gui, 'HandleVisibility', 'off')
close all
set(run_gui, 'HandleVisibility', 'on')
clc

clc
warning('off', 'all');

delete('alphabets_predicted.xlsx');
delete('out.txt');

if exist('Characters','dir')
    rmdir Characters s
end

global im filename
[filename, pathname] = uigetfile('*.jpg', 'Select an image', 'Input Image');
im = imread([pathname filename]);
figure(1), imshow(im); title('Input Image');

set(handles.pushbutton2, 'Enable', 'on');


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global im filename
try
    % Use Sauvola local adaptive binarization for textured media (palm-leaf manuscripts)
    bw = sauvola_binarize(im, 25, 0.25, 128);
    if ~exist('Denoised Image', 'dir')
        mkdir('Denoised Image');
    end
    imwrite(bw, fullfile('Denoised Image', filename));
catch
    gim = rgb2gray(im);
    T = adaptthresh(gim, 0.5);
    bw = imbinarize(gim, T);
    imwrite(bw, fullfile('Denoised Image', filename));
end

im = imread(fullfile('Denoised Image', filename));
figure(2), imshow(im); title('Denoised Image (Sauvola Binarized)');
    
set(handles.pushbutton2, 'Enable', 'off');
set(handles.pushbutton3, 'Enable', 'on');



% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global im
PEAK_DELTA_FACTOR = 6;
bw = im2bw(im);
bw_trans = (bw(:,2:end) - bw(:,1:end-1)) ~= 0;
im_hist = sum(bw_trans,2);
im_hist = medfilt1(im_hist);
[max_peaks, ~] = peakdet(im_hist, floor(max(im_hist)/PEAK_DELTA_FACTOR)); 

x = 1:1:size(im,2);
figure(3); imshow(im); hold on
plot(x, repmat(max_peaks(:,1), [1, size(im,2)]), '-g');
% plot(x, repmat(min_peaks(:,1), [1, size(im,2)]), '-r');
hold off;

grayImage = rgb2gray(im);
binaryImage = grayImage < 175;
binaryImage = imdilate(binaryImage, true(3));
binaryImage = bwareaopen(binaryImage, 100);
measurements = regionprops(binaryImage, {'Area', 'BoundingBox'});
allBoundingBox = cat(1, measurements.BoundingBox);

cnt = 1;
bbcopy = allBoundingBox;

D = pwd;
F = 'Characters';
if ~exist(fullfile(D,F),'dir')
    mkdir(fullfile(D,F))
end
    
figure(4), imshow(im); title('Segmented Characters'); hold on;

for i = 1 : size(max_peaks,1)
    ypt = bbcopy(:,2);
    ypos = find(ypt < max_peaks(i,1));
    
    sF = fullfile(D,F,sprintf('Line%d',i));
    if ~exist(sF,'dir')
        mkdir(sF)
    end
    
    for j = 1 : size(ypos,1)         
        [thisCh, pos] = imcrop(im, bbcopy(ypos(j),:));
        ch = sprintf('%s/%d.bmp', sF, cnt);
        imwrite(thisCh, ch); cnt = cnt + 1;
        x = [pos(1) pos(1)+pos(3) pos(1)+pos(3) pos(1) pos(1)];
        y = [pos(2) pos(2) pos(2)+pos(4) pos(2)+pos(4) pos(2)];
        plot(x, y, 'LineWidth', 2);
    end
    bbcopy(ypos,:) = [];
end
pause(0.0001);

set(handles.pushbutton3, 'Enable', 'off');
set(handles.pushbutton4, 'Enable', 'on');


% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global test_features lineNo
addpath('feature_extraction');
files = dir('Characters');
dirFlags = [files.isdir];
subFolders = files(dirFlags);
N = natsortfiles({subFolders.name});  
subFolders(1:2) = [];
cnt = 1;
for fcnt = 1 : length(subFolders)
    cfilename = dir(sprintf('Characters/%s/', subFolders(fcnt).name));
    N = natsortfiles({cfilename.name});
    for icnt = 2 : length(N)-1
        filename = N{1,icnt};
        imfiname = sprintf('Characters/%s/%s', subFolders(fcnt).name, filename);
        im = imread(imfiname);
        %%
        test_features(cnt,:) = feature_extractor(im);
        %%
        lineNo(1,cnt) = fcnt;
        cnt = cnt + 1;
    end
end
uiwait(msgbox('FEATURES EXTRACTED', 'INFO', 'help'));

set(handles.pushbutton4, 'Enable', 'off');
set(handles.pushbutton5, 'Enable', 'on');


% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global test_features lineNo

load data_features
u = unique(Group);
R = arrayfun(@(x)Group==u(x),1:numel(u),'un',0);
T = +vertcat(R{:});

net = trainSoftmaxLayer(data_features', T, 'ShowProgressWindow', 0);

Y = net(test_features');
idx = vec2ind(Y);

%%
[~, ~, raw] = xlsread('alphabets_malayalam.xlsx',1);
colA = raw(idx(:),1);
rowA = colA'; 
xlswrite('alphabets_predicted.xlsx', rowA, 1);

[~, ~, rwoA] = xlsread('alphabets_predicted.xlsx',1);
ulineNo = unique(lineNo);
for i = 1 : length(ulineNo)
    j = find(lineNo == i);
    newL(i,1:length(j)) = rwoA(j);
end
xlswrite('alphabets_predicted.xlsx', newL, 2);

%%
combine_characters

if exist('out_raw.txt', 'file')
    raw_str = fileread('out_raw.txt');
else
    raw_str = '';
end
if exist('out.txt', 'file')
    corr_str = fileread('out.txt');
else
    corr_str = '';
end

message = sprintf('OUTPUT SAVED IN ''out.txt''\n\nRaw Predicted Characters:\n%s\n\nMeaningful Word (Dictionary Corrected):\n%s', strtrim(raw_str), strtrim(corr_str));
uiwait(msgbox(message, 'OCR & WORD POST-PROCESSING COMPLETE', 'help'));

% Automatically trigger animated word transformation
try
    animate_word_transformation(strtrim(raw_str), 'malayalam_dictionary.txt');
catch
end

set(handles.pushbutton5, 'Enable', 'off');



% --- Executes on button press in pushbutton7.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

addpath('feature_extraction');
[filename, pathname] = uigetfile('*.bmp', 'Select a character to compute accuracy', 'Datalphabets');
im = imread([pathname filename]);

test_features = feature_extractor(im);

load data_features
u = unique(Group);
R = arrayfun(@(x)reshape(Group,1,[])==u(x),1:numel(u),'un',0);
Ts = +vertcat(R{:});

netr = trainSoftmaxLayer(data_features', Ts, 'MaxEpochs', 447, 'ShowProgressWindow', 0);
[~, predictedLabels] = max(netr(data_features'));
[~, cnnL] = max(netr(test_features));

trueLabels = Group;
C = confusionmat(trueLabels, predictedLabels);

uniqueClasses = unique(trueLabels);
numClasses = length(uniqueClasses);
classAccuracies = zeros(numClasses, 1);

for i = 1 : numClasses
    TP = C(i, i);
    totalInstancesOfClass = sum(trueLabels == uniqueClasses(i));
    
    if totalInstancesOfClass > 0
        classAccuracies(i) = (TP / totalInstancesOfClass) * 100;
    else
        classAccuracies(i) = NaN;
    end
end

classAccuracy = classAccuracies(cnnL);
message = sprintf('ACCURACY FOR SELECTED CLASS = %.2f%%', classAccuracy);
uiwait(msgbox(message, 'INFO', 'help'));


% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

delete('alphabets_predicted.xlsx');
delete('out.txt');

if exist('Characters','dir')
    rmdir Characters s
end

close all
clear
clc


% --- Helper function: Trigger Animated Word Transformation
function trigger_animate_word_transformation()
    if exist('out_raw.txt', 'file')
        raw_txt = fileread('out_raw.txt');
    else
        raw_txt = 'No characters detected';
    end

    animate_word_transformation(strtrim(raw_txt), 'malayalam_dictionary.txt');


% --- Helper function: Launch Accuracy Benchmark Suite
function trigger_evaluate_accuracy()
    evaluate_accuracy();


% --- Helper function: Launch Interactive Web Vibe Studio
function trigger_launch_web_studio()
    html_path = fullfile(pwd, 'web_studio', 'index.html');
    if exist(html_path, 'file')
        web(html_path, '-browser');
    else
        msgbox('Web Studio HTML file not found.', 'Error', 'error');
    end