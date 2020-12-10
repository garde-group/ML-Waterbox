! 0 is for Owen
! This program is made to calculate the diffusivity of specifically water


program diffusivity
        implicit none
        integer :: nuse, nskip, narg, i, nframe, ndone, uz, ret, &
         natoms, istep, j, c, k, v, pnum, na, coordnum
        real :: time, gbox(3,3), prec, bin, dx, dy, dz, length, &
         side
        character (len = 256) :: fname, xtcfile, arg(50), outfile
        real, allocatable :: coord(:), allcoord(:), diff(:)
        
        side = 3.99676 ! This is the side length of the box
        nuse = 5000 ! This is the number of frames to use (all of the frames)
        pnum = 2180 ! This is the number of particles
        na = 3 ! The number of atoms per particles
        nskip = 0 ! The number of frames to skip at the beginning
        outfile = 'diff.dat' ! The file the results will be written to
        ! Writing to the terminal to let the user know there is something happening
        write(*,*) ' '
        write(*,*) 'Diffusivity calculation started!!'
        write(*,*) ' '   

        ! This function reads in the user input that was given with the execution of the program
        narg = iargc()
        do i = 1, narg
                call getarg(i, arg(i))
        end do        

        ! If there are no arguments, then error out
        if (narg == 1) then
                write(*,*) 'Use flags -xtc -nskip -nuse'
                stop
        end if
        
        ! This reads in the information that was provided with the input of the program
        do i = 1, narg
                if(arg(i) == '-xtc') then
                        xtcfile = arg(i + 1) ! Reads in the .xtc file
                else if(arg(i) == '-o') then
                        outfile = arg(i + 1) ! Reads in the output files
                else if(arg(i) == '-nskip') then
                        read(arg(i + 1),*) nskip ! Number of frames to skip
                else if(arg(i) == '-nuse') then
                        read(arg(i + 1),*) nuse ! Number of frames to use
                else if(arg(i) == '-p') then
                        read(arg(i + 1),*) pnum ! Number of particles
                else if(arg(i) == '-s') then
                        read(arg(i + 1),*) side ! Side length of the box
                end if
        end do
        
        coordnum = pnum * na * 3 ! Calculates the total number of coordinates in the box
        allocate(coord(coordnum)) ! Allocates this array of coordinates
        v = coordnum * nuse ! The total number of coordinates over all frames 
        allocate(allcoord(v)) ! Allocate the allcoord array (a massive array of every single coordinate from every single frame)
        allcoord = 0 ! Initialize it to 0
        allocate(diff(nuse)) ! Allocate the diffusivity array based on the number of frames
        nframe = 0 ! Set both these to 0 as we have analyzed 0 frames
        open(unit = 10, file = outfile) ! Open the output file
        call xdrfopen(uz, xtcfile, 'r', ret) ! Using the xdrfopen, read in the file
        if (ret == 1) then ! If there are no errors in the files opening
                do while (ret == 1 .and. nframe < (nskip + nuse)) ! Do this for every frame
                        call readxtc(uz, natoms, istep, time, gbox, &
                        coord, prec, ret) ! Read in the file and the information into these specified variables
                        allcoord(1 + (nframe * coordnum) : (nframe+1) * &
                        coordnum) = coord ! The first 'chunk' of the array with the first frame, and continue to allocate the next frames to the next 'chunks'
                        nframe = nframe + 1 ! Increase the frame number
                end do
        else
                ! If there is an error, alert the user and quit the program
                write(*,*) 'Error in the xdrfopen'
                stop
        end if
        
        ! Initialize the array to 0
        diff = 0
        ! The goal of these nested loops is to determine the diffusivity. This is done by taking the distance between every particle to every other particle for every frame
        ! Each element of diff() represents the distance covered over that number of frames, e.g. diff(100) is the average distance of every particle to every other particle over 100 frames
        ! This first loop is the starting frame (i.e. what the other frames distances are calculated from)
        do i = 1, 5000
                ! This iterates over every particle
                do k = 1, 2180
                        ! This array is the frame that is calculated too. From frame i to frame j. It iterates over every frame to every other frame. Specifically the j do loop is the every other frame
                        do j = 0, 4998
                                if ((j+2+i)>=5000) exit ! This is just an error catcher to make sure they don't exceed the make number of frames
                                dx = abs(allcoord(9*k-8+j*coordnum) - allcoord(&
                                9*k-8+j*coordnum+coordnum*i)) ! This determines the x distance
                                dy = abs(allcoord(9*k-7+j*coordnum) - allcoord(&
                                9*k-7+j*coordnum+coordnum*i)) ! The y distance
                                dz = abs(allcoord(9*k-6+j*coordnum) - allcoord(&
                                9*k-6+j*coordnum+coordnum*i)) ! The z distances
                                length = dx**2+dy**2+dz**2 ! To total distance squared, see the root mean squared displacement formula
                                diff(i) = diff(i) + length ! Adds it to the respective frame different
                        end do
                end do
        end do
        
        do i = 1, size(diff)
                diff(i) = diff(i) / ((real(2180)) * real(5000 - i)) ! Averages the diffusivity distances
        end do
        do i = 1, size(diff) 
                write(10,*) i, diff(i) ! Writes the diffusivity information to the file
        end do

        ! Alerts the user the the calculations are done
        write(*,*) ' '
        write(*,*) 'Diffusivity calculation ended'
        write(*,*) ' '

! Ends the program
end program diffusivity     
