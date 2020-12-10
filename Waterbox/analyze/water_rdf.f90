! This is a program that takes in a .xtc file and outputs a .dat 
! file that can be used to calculate or graph the radial 
! distribution function
! Important note, due to array size and integer restrictions, the 
! optimum may be limited to accuracy of 1,000 frames

program rdf_calc
        ! Variables used for non-rdf calculation based operations
        implicit none
        integer :: narg, i, nframe, ndone, uz, ret, &
         natoms, istep
        real :: time, gbox(3,3), prec
        character (len = 256) :: xtcfile, arg(64), outfile
        real, allocatable :: coord(:)
        ! Variables unique to this calculation
        real, parameter :: pi = 3.14159265
        real :: bin, dx, dy, dz, length, side
        integer :: pnum, maxbins, na, ncoord, tatom, nuse, nskip, &
         j, c, k
        real, allocatable :: rdf(:), calcdist(:), rrdf(:)


        ! Default settings
        bin = 0.01 ! Bin size (in nm)
        side = 3.99676 ! Side length of box (in nm)
        nuse = 10 ! Number of frames to use
        pnum = 2180 ! The number of particles/molecules to be calculated 
        na = 3 ! The number of atoms per particle
        nskip = 0 ! Number of frames to be skipped'
        outfile = 'gofr.dat' ! Name of file to write to
        write(*,*) ' '
        write(*,*) 'Diffusivity calculation started!!'
        write(*,*) ' '   

        ! This do loop reads in the flags that are run with the file
        narg = iargc()
        do i = 1, narg
                call getarg(i, arg(i))
        end do        

        ! If there are no flags, error out and inform user
        if (narg == 1) then
                write(*,*) 'Use flags'
                stop
        end if
        
        ! This loop checks the flags of the input and assigns the values
        do i = 1, narg
                if(arg(i) == '-xtc') then
                        xtcfile = arg(i + 1)
                else if(arg(i) == '-bin') then
                        read(arg(i + 1),*) bin
                else if(arg(i) == '-o') then
                        outfile = arg(i + 1)
                else if(arg(i) == '-nskip') then
                        read(arg(i + 1),*) nskip
                else if(arg(i) == '-nuse') then
                        read(arg(i + 1),*) nuse
                else if(arg(i) == '-p') then
                        read(arg(i + 1),*) pnum
                else if(arg(i) == '-s') then
                        read(arg(i + 1),*) side
                else if(arg(i) == '-a') then
                        read(arg(i + 1),*) na
                end if
        end do
        
        ! The total number of atoms is the number of particles multiplied by
        ! the number of atoms per particle
        tatom = pnum * na 
        ncoord = tatom * 3 ! There are 3 coordinates per atoms --> ncoord
        ! The length is just used to allocate a large enough array for the rdf
        length = side * 2
        ! This is the maximum amount of bins, used to allocate the rdf
        maxbins = ceiling(length/bin)
        ! Each index of the rdf array represents one bin, however big the bin 
        ! is
        allocate(rdf(maxbins))
        ! This just sets the default rdf to 0
        rdf = 0 
        allocate(coord(ncoord))
        ! The number of frames analyzed is 0, hence nframe = 0
        nframe = 0
        ndone = 0
        ! This opens the file that the data is written to
        open(unit = 10, file = outfile)
        ! This opens the .xtc file
        call xdrfopen(uz, xtcfile, 'r', ret)
        ! If there are no errors in opening the file 
        if (ret == 1) then
                ! Do the analysis over the number of frames specified
                do while (ret == 1 .and. nframe < (nskip + nuse))
                        ! This writes a variety of useful information from 
                        ! the .xtc file to various variables
                        call readxtc(uz, natoms, istep, time, gbox, &
                        coord, prec, ret)
                        ! In order to calculate the rdf, the distance from 
                        ! every (for O-O) molecule to every other molecule
                        ! must be calculated. This next section iterates 
                        ! through the array of coordinates and calculates 
                        ! the distance from the 1st oxygen to every other 
                        ! one, then the 2nd and the 3rd and so on.
                        ! This do loop is the first part and selects the
                        ! 'first' molecule to calculate the distances from
                        ! This increases by 9 because the x coordinate of 
                        ! the oxygen is every 9 (3 for O then 3 for H then 3 for H)
                        do i = 1, ncoord, 9
                                ! Calcdist is an array of the calculated distances
                                ! This clears it everytime there is a new starting
                                ! atom to calculate the other distances to.
                                ! This can be done because in this do loop it 
                                ! accounts for the distances and stores them in the
                                ! rdf array in their specific bin
                                if (allocated(calcdist)) deallocate(calcdist)
                                allocate(calcdist(ncoord))
                                ! Sets every value to 0
                                calcdist = 0
                                ! This is the do loop that starts with the 'starting'
                                ! (i) atom and calculates the distances to every other
                                ! atom. This saves memory by starting at the i'th atom.
                                ! This loop increases by 9 for the same reason as above,
                                ! to only count the Oxygens, not every atom
                                do k = i + 9, ncoord, 9
                                        ! Finds the magnitude of the x difference
                                        dx = abs(coord(i) - coord(k))
                                        ! Finds the magnitude of the y difference
                                        dy = abs(coord(i + 1) - coord(k + 1))
                                        ! Finds the magnitude of the z difference
                                        dz = abs(coord(i + 2) - coord(k + 2))
                                        ! These if statements are to adjust for periodic
                                        ! boundary conditions. i.e. if the distance is 
                                        ! greater than half the side length, then the 
                                        ! 'image' box particle is closer and the distance
                                        ! is now subtracted from the side length
                                        if (dx > 0.5 * side) dx = dx - side
                                        if (dy > 0.5 * side) dy = dy - side
                                        if (dz > 0.5 * side) dz = dz - side
                                        ! Distance formula to calculate 3D point distances
                                        calcdist(k) = sqrt(dx**2+dy**2+dz**2)
                                end do
                                ! This do loop 'places' the distance into its bin. It takes 
                                ! the distance and adds one to the number of particles in 
                                ! the bin number
                                do j = 1, size(calcdist)
                                        ! Since calcdist is set to 0 and is only assigned
                                        ! every 9 times, all the zero distances can be 
                                        ! excluded from the bin calculation
                                        if (calcdist(j) == 0) cycle
                                        ! c is the bin number the distance falls into
                                        c = floor(calcdist(j) / bin) + 1
                                        ! Adding one to the number of distances in said bin
                                        rdf(c) = rdf(c) + 1
                                end do
                        end do
                        ! Prints what frame it's on to help user ensure everything is going
                        ! properly
                        print *, nframe
                        ! Adds one to the frame, since the program is advancing one frame
                        nframe = nframe + 1
                        ! Not really sure if ndone is needed. Pretty sure this code does 
                        ! nothing, but I'll leave it it, cause why not. 
                        if (nframe > nskip .and. nframe < (nskip + nuse)) then
                                ndone = ndone + 1
                        end if
                end do
        else
                ! If there was an error in opening the .xtc file
                write(*,*) 'Error in the xdrfopen'
                stop
        end if
        ! rrdf is similar to rdf (same size) but contains the adjusted values. I foudn it useful
        ! to make two arrays for debugging purposes and to help further understand exactly what 
        ! was happening
        allocate(rrdf(size(rdf)))
        do i = 1, size(rdf)
                ! Adjustment to convert the number of atoms at a certain distance to the adjusted
                ! number of atoms per bin 
                rrdf(i) = rdf(i) / (sum(rdf) / (real(tatom)))
                ! Now that the atoms per bin is correct, the bin must be adjusted for volume. By dividing each
                ! by the volume they take up, a standard density is derived. 
                rrdf(i) = real(rrdf(i)) / ((4./3. * pi * (((bin * real(i)) ** 3) - (bin * (real(i) - 1.)) ** 3)))
                ! Now, to make the g(r), it must be compared to the bulk, the denisty of which is the total 
                ! number of atoms in the box divided by the volume of the box
                rrdf(i) = rrdf(i) / real((tatom) / side ** 3)
        end do
        ! Now this code must be written to the designated output file
        do i = 1, size(rdf)
                write(10,*) bin * i, rrdf(i), rdf(i)
        end do

        write(*,*) ' '
        write(*,*) 'Probability of binding calculation ended'
        write(*,*) ' '
        
end program rdf_calc     
