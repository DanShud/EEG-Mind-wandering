% CURRY 9 M-file, Platform: PCWIN, Created on: 11/27/2024 3:54:14 PM
%
% data filename without extension
%export_cdt_as_csv(varargin)

function export_cdt_as_csv(varargin)
    DataFile = [varargin{1},'.cdt'];
    ParameterFile = [DataFile,'.dpa'];
    LabelFile = [DataFile,'.dpa'];
    EventFile = [DataFile,'.cef'];

    disp(DataFile)

        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % open parameter file
    fid = fopen(ParameterFile,'rt');
    cell = textscan(fid,'%s','whitespace','','endofline','§');
    fclose(fid);
    cont = cell2mat(cell{1});
    
    % read parameters from parameter file
    % tokens (second line is for Curry 6 notation)
    tok = { 'NumSamples'; 'NumChannels'; 'NumTrials'; 'SampleFreqHz';  'TriggerOffsetUsec';  'DataFormat'; 'DataSampOrder';   'SampleTimeUsec'; 
            'NUM_SAMPLES';'NUM_CHANNELS';'NUM_TRIALS';'SAMPLE_FREQ_HZ';'TRIGGER_OFFSET_USEC';'DATA_FORMAT';'DATA_SAMP_ORDER'; 'SAMPLE_TIME_USEC' };
    
    % scan in cell 1 for keywords - all keywords must exist!
    nt = size(tok,1);
    a = zeros(nt,1);
    for i = 1:nt
         ctok = tok{i,1};
         ix = strfind(cont,ctok);
         if ~isempty ( ix )
             text = sscanf(cont(ix+numel(ctok):end),' = %s');     % skip =
             if strcmp ( text,'ASCII' ) || strcmp ( text,'CHAN' ) % test for alphanumeric values
                 a(i) = 1;
             else 
                 c = sscanf(text,'%f');         % try to read a number
                 if ~isempty ( c )
                     a(i) = c;                  % assign if it was a number
                 end
             end
         end 
    end
    
    % derived variables. numbers (1) (2) etc are the token numbers
    nSamples    = a(1)+a(1+nt/2);
    nChannels   = a(2)+a(2+nt/2);
    nTrials     = a(3)+a(3+nt/2);
    fFrequency  = a(4)+a(4+nt/2);
    fOffsetUsec = a(5)+a(5+nt/2);
    nASCII      = a(6)+a(6+nt/2);
    nMultiplex  = a(7)+a(7+nt/2);
    fSampleTime = a(8)+a(8+nt/2);
    
    if ( fFrequency == 0 && fSampleTime ~= 0 )
        fFrequency = 1000000 / fSampleTime;
    end    
    
    %Search for Impedance Values
    tixstar = strfind(cont,'IMPEDANCE_VALUES START_LIST');
    tixstop = strfind(cont,'IMPEDANCE_VALUES END_LIST');
    
    impedancelist = []; 
    impedancematrix = [];
    
    if (~isempty(tixstar)) && (~isempty(tixstop))
        text = cont(tixstar:tixstop-1);
        tcell = textscan(text,'%s');
        tcell = tcell{1,1};
        for tcC = 1:size(tcell,1)
           tcell{tcC} = str2num(tcell{tcC}); % data was read in as strings - force to numbers
           if ~isempty(tcell{tcC}) % skip if it is not a number
               impedancelist(end+1) = tcell{tcC};
           end
        end
    
        % Curry records last 10 impedances
        impedancematrix = reshape(impedancelist,[(size(impedancelist,2)/10),10])';
        impedancematrix(impedancematrix == -1) = NaN; % screen for missing
    end
                
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % open label file
    fid = fopen(LabelFile,'rt');
    cell = textscan(fid,'%s','whitespace','','endofline','§');
    fclose(fid);
    cont = cell2mat(cell{1});
    
    % read labels from label file
    % initialize labels
    labels = num2cell(1:nChannels);
    
    for i = 1:nChannels
        text = sprintf('EEG%d',i);
        labels(i) = cellstr(text);
    end
    
    % scan in cell 1 for LABELS (occurs four times per channel group)
    ix = strfind(cont,[char(10),'LABELS']);
    nt = size(ix,2);
    nc = 0;
    
    for i = 4:4:nt                                                      % loop over channel groups
        newlines = ix(i-1) + strfind(cont(ix(i-1)+1:ix(i)),char(10));   % newline
        last = nChannels - nc;
        for j = 1:min(last,size(newlines,2)-1)                          % loop over labels
            text = cont(newlines(j)+1:newlines(j+1)-1);
            if isempty(strfind(text,'END_LIST'))
                nc = nc + 1;
                labels(nc) = cellstr(text);
            else 
                break
            end
        end 
    end
    
    % read sensor locations from label file
    % initialize sensor locations
    sensorpos = zeros(3,0);
    
    % scan in cell 1 for SENSORS (occurs four times per channel group)
    ix = strfind(cont,[char(10),'SENSORS']);
    nt = size(ix,2);
    nc = 0;
    
    for i = 4:4:nt                                                      % loop over channel groups
        newlines = ix(i-1) + strfind(cont(ix(i-1)+1:ix(i)),char(10));   % newline
        last = nChannels - nc;
        for j = 1:min(last,size(newlines,2)-1)                          % loop over labels
            text = cont(newlines(j)+1:newlines(j+1)-1);
            if isempty(strfind(text,'END_LIST'))
                nc = nc + 1;
                tcell = textscan(text,'%f');                           
                posx = tcell{1}(1);
                posy = tcell{1}(2);
                posz = tcell{1}(3);
                sensorpos = cat ( 2, sensorpos, [ posx; posy; posz ] );
            else 
                break
            end
        end 
    end
    
    %Search for Epoch Labels
    tixstar = strfind(cont,'EPOCH_LABELS START_LIST');
    tixstop = strfind(cont,'EPOCH_LABELS END_LIST');
    
    epochlabelslist = []; 
    
    if (~isempty(tixstar)) && (~isempty(tixstop))
        text = cont(tixstar:tixstop-1);
        tcell = textscan(text,'%s', 'delimiter','\n','whitespace','', 'headerlines', 1);
        epochlabelslist = tcell{1,1};
    end
    
    %Search for Epoch Information
    tixstar = strfind(cont,'EPOCH_INFORMATION START_LIST');
    tixstop = strfind(cont,'EPOCH_INFORMATION END_LIST');
    
    epochinformationlist = []; 
    
    if (~isempty(tixstar)) && (~isempty(tixstop))
        text = cont(tixstar:tixstop-1);
        tcell = textscan(text,'%d%d%d%d%d%d%d', 'delimiter','\n','headerlines', 1);
        epochinformationlist = cell2mat(tcell);
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % read events from event file
    % initialize events
    ne = 0;                                                             % number of events
    events = zeros(4,0);
    annotations = cellstr('empty');
    
    % find appropriate file
    fid = fopen(EventFile,'rt');
    
    if fid >= 0
        cell = textscan(fid,'%s','whitespace','','endofline','§');
        fclose(fid);
        cont = cell2mat(cell{1});
    
        % scan in cell 1 for NUMBER_LIST (occurs five times)
        ix = strfind(cont,'NUMBER_LIST');
        
        newlines = ix(4) - 1 + strfind(cont(ix(4):ix(5)),char(10));     % newline
        last = size(newlines,2)-1;
        for j = 1:last                                                  % loop over labels
            text = cont(newlines(j)+1:newlines(j+1)-1);
            tcell = textscan(text,'%d');                           
            sample = tcell{1}(1);                                       % access more content using different columns
            type = tcell{1}(3);
            startsample = tcell{1}(5);
            endsample = tcell{1}(6);
            ne = ne + 1;
            events = cat ( 2, events, [ sample; type; startsample; endsample ] );
        end
        
        % scan in cell 1 for REMARK_LIST (occurs five times)
        ix = strfind(cont,'REMARK_LIST');
        na = 0;
        
        newlines = ix(4) - 1 + strfind(cont(ix(4):ix(5)),char(10));     % newline
        last = size(newlines,2)-1;
        for j = 1:last                                                  % loop over labels
            text = cont(newlines(j)+1:newlines(j+1)-1);
            na = na + 1;
            annotations(na) = cellstr(text);
        end    
    end
    
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % read data file
    if nASCII == 1
        fid = fopen(DataFile,'rt');
        cell = textscan(fid,'%f',nChannels*nSamples*nTrials);
        fclose(fid);
        data = reshape([cell{1}],nChannels,nSamples*nTrials);
    else
        fid = fopen(DataFile,'rb');
        data = fread(fid,[nChannels,nSamples*nTrials],'float32');
        fclose(fid);
    end
    
    % transpose?
    if nMultiplex == 1
        data = data';
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % time axis
    time = linspace(fOffsetUsec/1000,fOffsetUsec/1000+(nSamples*nTrials-1)*1000/fFrequency,nSamples*nTrials);
    
    writematrix(data.', strcat(DataFile,"_data.csv"))
    events_transpose = events.';

% fprintf('The size of the matrix is: %s', num2str(size(events_transpose)),num2str(size([ 'sample','type','startsample','endsample' ])))

   
    writematrix(events_transpose, strcat(DataFile,'_events.csv'))
    
    
    % simple plot
   % subplot(2,1,1);
   % plot(time,data);  
    
    % stacked plot
   % subplot(2,1,2);
    %range = max([abs(min(min(data))) abs(max(max(data)))]);
    %shift = linspace((nChannels-1)*range*0.3,0,nChannels);
    %plot(time,data+repmat(shift,nSamples*nTrials,1)');
    %set(gca,'ytick',flip(shift),'yticklabel',flip(labels),'GridLineStyle',':','XGrid','on','YGrid','off');
    %ylim([min(min(data+repmat(shift,nSamples*nTrials,1)')) max(max(data+repmat(shift,nSamples*nTrials,1)'))]);
end


